from setuptools import setup, find_packages

VERSION = '0.1.5'
DESCRIPTION = 'A basic package to calculate sma and rsi indicators'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
# Setting up
setup(
    name="sma_rsi_indicators",
    version=VERSION,
    author="yavuzselimvurgun",
    author_email="<yavuzselim.vurgun@bahcesehir.edu.tr>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'sma', 'rsi', 'csv'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)