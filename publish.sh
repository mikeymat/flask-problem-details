#!/bin/bash
python -m pip install --upgrade build
python -m build
python -m pip install --upgrade twine    
python3 -m twine upload --repository pypi dist/*
rm -rf ./dist       
