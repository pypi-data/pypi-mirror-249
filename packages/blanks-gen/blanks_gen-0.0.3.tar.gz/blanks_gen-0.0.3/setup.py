from setuptools import setup


def get_version():
    version = {}
    with open("blanks_gen/version.py") as f:
        exec(f.read(), version)
    return version["__version__"]


long_description = """blanks_gen is a script that wraps tectonic
to generate blanks for [Chgk](https://en.wikipedia.org/wiki/What%3F_Where%3F_When%3F)

Project home on gitlab: https://gitlab.com/peczony/blanks_gen
"""


setup(
    name="blanks_gen",
    version=get_version(),
    author="Alexander Pecheny",
    author_email="ap@pecheny.me",
    description="blanks_gen is a script that wraps tectonic to generate blanks for [Chgk](https://en.wikipedia.org/wiki/What%3F_Where%3F_When%3F)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peczony/blanks_gen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["blanks_gen"],
    package_data={
        "blanks_gen": [
            "resources/*.tex",
            "resources/*.yaml",
        ]
    },
    entry_points={"console_scripts": [
        "blanks_gen = blanks_gen.__main__:main",
    ]},
    install_requires=["pecheny_utils", "pypdf", "PyYAML"],
)
