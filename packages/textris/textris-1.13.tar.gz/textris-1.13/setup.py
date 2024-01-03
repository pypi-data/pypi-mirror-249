##setup

from setuptools import setup, find_packages

setup(name="textris",version=1.13,packages=find_packages(),
      install_requires=["windows-curses>=2.3.1","keyboard>=0.13.5"],
      entry_points={"console_scripts": ["textris=textris:func"]})