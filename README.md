# prim

```
python -m ensurepip --user
python -m pip install --user --upgrade pip
python -m pip install --user --upgrade virtualenv
python -m virtualenv primvenv
python setup.py develop
python prim/lexer.py test/hello-world.pr
python prim/parser.py test/hello-world.pr
```