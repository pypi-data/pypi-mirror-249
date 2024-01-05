#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import shutil
import subprocess
import sys
from functools import partial
from pathlib import Path
from typing import NamedTuple, Optional

import pypdf
import yaml
from pecheny_utils import (
    download_file,
    escape_latex,
    find_font,
    get_tectonic_path,
    get_utils_dir,
    install_tectonic,
)

_open = partial(open, encoding="utf8")
EMPTY_NAME = "~"
RAW_PREFIX = "raw_tex:"
DEFAULT_FONT = "OpenSans-Light.ttf"


class Cell(NamedTuple):
    team_number: int
    team_name: Optional[str]
    question_number: Optional[int]


def read_text(path):
    return Path(path).read_text(encoding="utf8").replace("\r", "")


def get_resource_dir():
    if getattr(sys, "frozen", False):
        sourcedir = os.path.dirname(sys.executable)
    else:
        sourcedir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    resourcedir = os.path.join(sourcedir, "resources")
    return resourcedir


def add_crops(crops_file, regular_file):
    crops = pypdf.PdfReader(open(crops_file, "rb"))
    reg = pypdf.PdfReader(open(regular_file, "rb"))
    crops_page = crops.pages[0]

    output_pdf = pypdf.PdfWriter()
    for i, page in enumerate(reg.pages):
        output_pdf.add_page(page)
        output_pdf.pages[i].merge_page(crops_page)

    with open(regular_file, "wb") as output_file:
        output_pdf.write(output_file)


class BlanksGen:
    def __init__(self, args):
        self.args = args
        self.tmp_files = []
        if args.config:
            if os.path.isabs(args.config):
                self.config_dir = os.path.dirname(os.path.abspath(args.config))
                self.config = yaml.safe_load(read_text(args.config))
            else:
                abspaths_to_try = [
                    os.path.abspath(os.path.join(os.getcwd(), args.config)),
                    os.path.abspath(os.path.join(get_resource_dir(), args.config)),
                ]
                for path in abspaths_to_try:
                    if os.path.isfile(path):
                        self.config_dir = os.path.dirname(os.path.abspath(path))
                        self.config = yaml.safe_load(read_text(path))
                        break
        else:
            self.config_dir = get_resource_dir()
            self.config = yaml.safe_load(
                read_text(os.path.join(self.config_dir, "default_config.yaml"))
            )
        assert args.team_names or args.teams
        cwd = os.getcwd()
        os.chdir(self.config_dir)
        selected_font = args.font or self.config["font_name"]
        if selected_font == DEFAULT_FONT:
            try:
                found_font = find_font(selected_font)
            except:
                download_file(
                    "https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-Light.ttf"
                )
                shutil.move(
                    "OpenSans-Light.ttf", os.path.join(get_utils_dir(), "fonts")
                )
                found_font = find_font(selected_font)
            shutil.copy(found_font, self.args.output_folder)
            self.tmp_files.append(os.path.join(self.args.output_folder, selected_font))
        self.prefix = read_text(self.config["prefix"]).replace(
            "FONTNAME", selected_font
        )
        self.cell_stub = read_text(self.config["cell"])
        self.postfix = read_text(self.config["postfix"])
        if self.config.get("crops"):
            self.crops_file = os.path.abspath(self.config["crops"])
        else:
            self.crops_file = None
        os.chdir(cwd)
        tectonic_path = get_tectonic_path()
        if not tectonic_path:
            print("tectonic is not present, installing it...")
            install_tectonic()
            tectonic_path = get_tectonic_path()
        if not tectonic_path:
            raise Exception("tectonic couldn't be installed successfully :(")
        if args.debug:
            print(f"tectonic found at `{tectonic_path}`")
        self.tectonic_path = tectonic_path

    def make_row(self, row: list[Cell]):
        cells = []
        for cell in row:
            new_cell = (
                self.cell_stub.replace("TEAMNUMBER", str(cell.team_number))
                .replace("TEAMNAME", cell.team_name)
                .replace(
                    "QUESTIONNUMBER",
                    str(cell.question_number)
                    if cell.question_number
                    else self.config["blank_question_number"],
                )
            )
            cells.append(new_cell)
        sep = self.config["hsep_stub"].replace("<HSEP>", self.config["hsep"])
        return sep.join(cells)

    def make_page(self, batch):
        rows = []
        row_len = self.config["columns"]
        while batch:
            row_, batch = batch[:row_len], batch[row_len:]
            rows.append(self.make_row(row_))
        sep = self.config["vsep_stub"].replace("<VSEP>", self.config["vsep"])
        page = (
            (self.config.get("page_prefix") or "")
            + sep.join(rows)
            + (self.config.get("page_postfix") or "")
        )
        return page

    def make_file(self, cells, file_name):
        with _open(file_name, "w") as f:
            f.write(self.prefix)
            pages = []
            cells_per_page = self.config["rows"] * self.config["columns"]
            while cells:
                page, cells = cells[:cells_per_page], cells[cells_per_page:]
                pages.append(self.make_page(page))
            f.write(self.config["page_sep"].join(pages))
            f.write(self.postfix)

    def wrap_name(self, name):
        name = name.strip()
        if name.startswith(RAW_PREFIX):
            return name[len(RAW_PREFIX) :].strip()
        return escape_latex(name)

    def generate_cells(self):
        args = self.args
        if args.team_names:
            team_names = [
                self.wrap_name(x)
                for x in read_text(args.team_names).split("\n")
                if x.strip()
            ]
        else:
            team_names = [EMPTY_NAME for _ in range(args.teams)]
        cells_per_list = self.config["rows"] * self.config["columns"]
        if self.config.get("batch_mode"):
            result = []
            team_names = list(enumerate(team_names))
            while team_names:
                team_batch, team_names = (
                    team_names[:cells_per_list],
                    team_names[cells_per_list:],
                )
                cells = []
                for i in range(args.questions):
                    for n, team in team_batch:
                        cells.append(
                            Cell(
                                team_number=n + 1, team_name=team, question_number=i + 1
                            )
                        )
                for _ in range(args.zero_questions):
                    for n, team in team_batch:
                        cells.append(
                            Cell(
                                team_number=n + 1, team_name=team, question_number=None
                            )
                        )
                result.append(cells)
            return result
        else:
            cells = []
            for n, team in enumerate(team_names):
                for i in range(args.questions):
                    cells.append(
                        Cell(team_number=n + 1, team_name=team, question_number=i + 1)
                    )
                for _ in range(args.zero_questions):
                    cells.append(
                        Cell(team_number=n + 1, team_name=team, question_number=None)
                    )
            return [cells]

    def make(self):
        args = self.args
        if not os.path.isdir(args.output_folder):
            os.makedirs(args.output_folder, exist_ok=True)

        batches = self.generate_cells()

        for i, batch in enumerate(batches):
            file_name = os.path.join(
                args.output_folder, f"batch_{str(i + 1).zfill(3)}.tex"
            )
            file_name_pdf = os.path.splitext(file_name)[0] + ".pdf"
            self.make_file(batch, file_name)
            subprocess.run(
                [self.tectonic_path, os.path.basename(file_name)],
                check=True,
                cwd=args.output_folder,
            )
            if self.crops_file:
                add_crops(self.crops_file, file_name_pdf)
            if not args.debug:
                os.remove(file_name)
                for tmp_file in self.tmp_files:
                    os.remove(tmp_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--team_names", "-tn")
    parser.add_argument("--teams", "-t", type=int)
    parser.add_argument("--output_folder", "-o")
    parser.add_argument("--config", "-c")
    parser.add_argument("--font", "-f")
    parser.add_argument("--questions", "-q", type=int, default=90)
    parser.add_argument("--zero_questions", "-z", type=int, default=0)
    args = parser.parse_args()

    if not args.team_names and not args.teams:
        print(
            "Either --team_names (path to file with team names) or --teams (number of teams) should be specified"
        )
        sys.exit(1)

    BlanksGen(args).make()


if __name__ == "__main__":
    main()
