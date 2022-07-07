# Generating distribution archives
```
python3 -m pip install --upgrade build
python3 -m build
```

# Uploading the distribution archives
```
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```