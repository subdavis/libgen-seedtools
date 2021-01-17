import os

from setuptools import find_packages, setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="libgen-seedtools",
    author="Brandon Davis",
    version="0.2.0",
    author_email="libgen-seedtools@subdavis.com",
    url="https://github.com/subdavis/libgen-seedtools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "click-aliases",
        "colorama",
        "humanfriendly",
        "ipfshttpclient",
        "pydantic",
        "pyjwt",
        "transmission-rpc",
        "requests",
        "requests-toolbelt",
        "torrentool",
        "torrent-tracker-scraper",
    ],
    license="MIT",
    entry_points={
        "console_scripts": ["libgen-seedtools = libgen_seedtools.cli:cli"],
    },
    python_requires=">=3.6",
    setup_requires=["setuptools-git"],
)
