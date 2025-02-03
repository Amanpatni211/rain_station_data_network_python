# Networks_rain_project/Projects/rain_station_data_network_python/setup.py
from setuptools import setup, find_packages

setup(
    name="rain_station",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
    ],
)