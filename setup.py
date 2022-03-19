from setuptools import setup

setup(
    name="zdbpydra",
    version="0.1.4",
    author="Donatus Herre",
    author_email="donatus.herre@slub-dresden.de",
    description="ZDB Hydra API Client",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    license="GPLv3",
    url="https://github.com/herreio/zdbpydra",
    packages=["zdbpydra"],
    install_requires=["requests"],
    entry_points={
      'console_scripts': ['zdbpydra = zdbpydra.__main__:main'],
    },
)
