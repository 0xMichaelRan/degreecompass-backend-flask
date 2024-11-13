# Setup

Use poetry to manage dependencies:

```
poetry new flask-degree-compass
cd flask-degree-compass
poetry add flask
vi app.py
poetry run python app.py 
# or poetry run flask run, but can't customize port
```

Config environment in VS Code:

Cmd + Shift + P, "Python Select Interpreter", and choose Poetry (with Python 3.11.X).

## TODO

* filter majors by subject and category.
* search majors by name.
* user login and register.
* Add LLM support for major details page, and persist this data. 
* Need a docker-compose file to run the database.
