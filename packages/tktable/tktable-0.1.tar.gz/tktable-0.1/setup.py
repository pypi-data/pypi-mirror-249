from setuptools import setup, find_packages

setup(
    name="tktable",
    version="0.1",
    author="Nitin Garg",
    description="A Simple Solution to easily use tables in any Tkinter Application",
    packages=find_packages(),
    install_requires=["ttkbootstrap>=1.10.1"]
)