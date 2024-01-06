import setuptools
# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="extended-selenium-page-factory",
    version="0.5beta",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="Extension for page factory.",
    url="https://github.com/alexgorji/extendedseleniumpagefactory.git",
    packages=setuptools.find_packages(),
    install_requires=['selenium-page-factory==2.6'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
