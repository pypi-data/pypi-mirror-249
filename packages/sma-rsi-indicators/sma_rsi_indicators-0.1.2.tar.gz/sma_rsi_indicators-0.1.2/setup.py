from setuptools import setup, find_packages

VERSION = '0.1.2'
DESCRIPTION = 'A basic package to calculate sma and rsi indicators'
LONG_DESCRIPTION = 'A package that allows you to calculate sma and rsi indicators from a given csv file and outputs the indicators to a given csv file.'

# Setting up
setup(
    name="sma_rsi_indicators",
    version=VERSION,
    author="yavuzselimvurgun",
    author_email="<yavuzselim.vurgun@bahcesehir.edu.tr>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'sma', 'rsi', 'csv'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)