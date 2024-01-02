### To test
```
virtualenv venv
. venv/bin/activate
pip install .
```
and then you can use commands like
```
ellipsis ping
```
and when you're done
```
deactivate
```


### To publish
Increment the version in `ellipsis/cli.py:CLI_VERSION` and in `pyproject.toml`.  Then push your changes to master. Then
```
# Note: Dont run this within the venv!
flit publish
```
Note: The GitHub workflow doesn't work at the moment.