import setuptools

setuptools.setup(
    name="extended-selenium-page-factory",
    version="0.1beta",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="Extension for page factory.",
    url="https://github.com/alexgorji/musicscore.git",
    packages=setuptools.find_packages(),
    install_requires=['selenium-page-factory==2.6'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
