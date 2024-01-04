# type: ignore
from setuptools import find_packages, setup

setup(
    name="hailstone_calculator",
    version="0.0.4",
    packages=find_packages(exclude=["tests*"]),
    license="MIT",
    description="Hailstone calculator",
    author="Ibrahim Animashaun",
    # use_scm_version=True,
    # setup_requires=['setuptools_scm'],
)
