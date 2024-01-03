## PyPI
- https://pypi.org/project/gpt-prive/

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
