# Dog Bed DB TODO

Simple example app to organize your every day tasks using Dob Bed db database from aosabook 500 lines or less.

## Install dependencies

```
pip install -r requirements.txt
```

## Run server

```
export FLASK_APP=dbdb_todo
export FLASK_ENV=development
flask run
```

## Run tests

Install teh application as a package.

```
python dbdb_todo/setup.py install
```

Run the tests

```
pytest test/
```