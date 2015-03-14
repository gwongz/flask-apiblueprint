Flask-APIBlueprint
==================

What is Flask-APIBlueprint?
-------------------------
Flask-APIBlueprint is a Flask micro-framework extension which adds support for
route inheritance for Blueprints.

If you're building an API with Blueprints in Flask, you don't have to redeclare the routes if using the `APIBlueprint` class. You can also override routes as you version your API and remap endpoints.

#### What do I need?

Flask. 


#### Where are the tests?

To run the tests use the `test_apiblueprint.py` file:

```
$ python test_apiblueprint.py
```

#### How do I implement this?

See the [docs](http://flask-apiblueprint.readthedocs.org/en/latest/)for how to construct and register an `APIBlueprint`. Or run the example:

```
$ python app.py

```

You'll need to `pip install Flask-SQLAlchemy` in order to run the example app.
