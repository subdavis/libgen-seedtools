import os
from setuptools import find_packages, setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='IPFS BitTorrent Mirror',
    author='Brandon Davis',
    version='0.1.0',
    author_email='pmir@subdavis.com',
    url="https://github.com/subdavis/ipfs-bittorrent-mirror",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "click-aliases",
        "colorama",
        "ipfshttpclient",
        "pydantic",
        "pyjwt",
        "qbittorrent-api",
        "requests",
        "requests-toolbelt",
        "torrentool",
    ],
    license='MIT',
    entry_points={'console_scripts': ['pmir = ipfs_bt_mirror:cli'],},
    python_requires='>=3.6',
    setup_requires=['setuptools-git'],
)