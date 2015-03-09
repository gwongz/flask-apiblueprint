Flask-APIBlueprint
==================

What is Flask-APIBlueprint?
-------------------------
Flask-APIBlueprint is a Flask micro-framework extension which adds support for
route inheritance for Blueprints.

If you're building an API with Blueprints in Flask, you don't have to redeclare the routes if using the `APIBlueprint` class. You can also override routes as you version your API and remap endpoints.

#### What do I need?

Flask. `pip` or `easy_install` will
install it for you if you do `pip install Flask-APIBlueprint`.
Using a [virtualenv](https://virtualenv.pypa.io/en/latest/) is encouraged.


#### Where are the tests?

To run the tests use the `test_apiblueprint.py` file:

```
$ python test_apiblueprint.py
```

#### How do I implement this?

```
# construct and register a blueprint
api_v1 = APIBlueprint('api_v1', __name__, subdomain='', url_prefix='/api/v1')
app.register(api_v1)

# construct a blueprint that inherits all routes from api_v1 blueprint
api_v2 = APIBlueprint('api_v2', __name__, subdomain='', url_prefix='/api/v2',inherit_from=api_v1, remapping=None)
app.register(api_v2)
```

With the `APIBlueprint` class you can also remap endpoints and override routes.
Refer to the [sample_api] for more detailed implementation or run the example:

```
$ python app.py
```

You'll need to `pip install Flask-SQLAlchemy` in order to run the example app. 
