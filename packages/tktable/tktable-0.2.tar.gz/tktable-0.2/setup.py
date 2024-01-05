from setuptools import setup, find_packages

with open("README.md","r") as fl:
    longdesc = fl.read()

setup(
    name="tktable",
    version="0.2",
    author="Nitin Garg",
    description="A Simple Solution to easily use tables in any Tkinter Application",
    long_description=longdesc,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["ttkbootstrap>=1.10.1"]
)