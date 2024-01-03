##setup

from setuptools import setup, find_packages

with open("README.txt","r") as file:
    description=file.read()

setup(name="textris",author="YknotTYD",version=1.18,packages=find_packages(),
      install_requires=["windows-curses>=2.3.1","keyboard>=0.13.5"],
      entry_points={"console_scripts": ["textris=textris:func"]},description=description)