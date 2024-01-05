# Introduction 
simple library to have some commonly used functions for everyday purpose 

# Getting Started
There are the following functionalities in this lib:
- filefunctions - some convienience functions for file handling

# Build and Test
1. Install virtual environment 
python3 -m venv .venv
source .venv/bin/activate
pip install build
pip install twine
pip install pytest

2. Build a package:
python3 -m build

3. Run the testcases  
pip install -e .
cd tests
pytest

4. Upload the package to pypi.org
python3 -m twine upload dist/*

Usage of basefunctions
```
import basefunctions as bf

bf.getCurrentDirectory()
'/home/user/development'

bf.getBaseName('/usr/local/bin/python3')
'python3'
```

# Project Homepage
https://dev.azure.com/neuraldevelopment/basefunctions

# Contribute
If you find a defect or suggest a new function, please send an eMail to neutro2@outlook.de
