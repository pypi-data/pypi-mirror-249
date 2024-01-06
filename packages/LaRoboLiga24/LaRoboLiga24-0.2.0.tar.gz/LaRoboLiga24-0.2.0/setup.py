import setuptools
from pathlib import Path

setuptools.setup(
    name='LaRoboLiga24',
    version='0.2.0',
    description="A OpenAI Gym Env for the event LaRoboLiga",
    long_description=Path("Readme.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="LaRoboLiga24*"),
    install_requires=['gym', 'pybullet', 'opencv-contrib-python', 'numpy']
)