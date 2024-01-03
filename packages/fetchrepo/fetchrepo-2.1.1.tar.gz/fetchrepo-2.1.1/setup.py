from setuptools import setup,find_packages

setup(
    name="fetchrepo",
    version="2.1.1",
    packages=find_packages(),
    author="Al-Fareed",
    description="Fetches and returns required content from github repository",
    long_description=open("README.md").read(),
    long_description_content_type = "text/markdown"
    )