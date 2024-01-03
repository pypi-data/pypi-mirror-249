## Project and PyPI Package 
- https://pypi.org/project/gpt-prive/
- https://github.com/gpt-prive
- https://huggingface.co/Slowblood

## Required Dependencies 
- build, twine

## Build
- Update `src/*` and update `setup.conf`
- Builds to `dist/` directory
```
python -m build
```
- Push to PyPi with twine
```
python -m twine upload --repository pypi dist/*
```

## Setup
- Create API key in PyPI account
- Add to `~/.pypirc`
```
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
  username = __token__
  password = pypi-AgszLCJ-Cut-And-P@aste-The-API-K#y-From-Your-AccountlZ7-mow

[testpypi]
repository = https://test.pypi.org/legacy/
```