"""
File:           setup.py
Last changed:   05/01/2024 11:43
Purpose:        Code configures the distribution of a Python package using setuptools, including package details 
Authors:        Fernando Antonio Marques Schettini      
Usage: 
	HowToExecute:   python3 setup.py sdist bdist_wheel
    HowToUpload: twine upload --repository-url https://upload.pypi.org/legacy/ -u __token__ -p your-token dist/*        
"""

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Find best cable positioning'
LONG_DESCRIPTION = 'Support tool, offers a set of Python classes designed for forecasting optimal wind turbine placements and efficient cable connections in wind energy systems.'

authors = ["Fernando Schettini", "Pedro Miranda"]
emails = "fernandoschettini@outlook.com"

# Setting up
setup(
    name="wamuu",
    version=VERSION,
    author=authors,
    author_email=emails,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'wind', 'energy', 'cable positioning', 'search algorithm', 'optimization'],
    classifiers=[
        "Development Status :: 1 - Planning",
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)