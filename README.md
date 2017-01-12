[![Build Status](https://travis-ci.org/gwongz/flask-apiblueprint.svg?branch=master)](https://travis-ci.org/gwongz/flask-apiblueprint)

Flask-APIBlueprint
==================

iWhat is Flask-APIBlueprint?
-------------------------
Flask-APIBlueprint is a Flask micro-framework extension which adds support for
route inheritance for Blueprints.

If you're building an API with Blueprints in Flask, you don't have to redeclare the routes if using the `APIBlueprint` class. You can also override routes as you version your API and remap endpoints.

#### What do I need?

Flask. It will automatically be installed if you install the extension via pip:

```
$ pip install flask-apiblueprint
```

To run tests or the sample, install the requirements in `requirements_dev.txt`:

```
$ pip install -r requirements_dev.txt
```

#### Where are the tests?

To run the tests use the `test_apiblueprint.py` file:

```
$ py.test test_apiblueprint.py
```

#### How do I implement this?

##### Inheritance
Use the `inherit_from` keyword argument in the `APIBlueprint` constructor to copy routes over from another `APIBlueprint`.

```
api_v2 = APIBlueprint(
    'api_v2', __name__, subdomain='', url_prefix='/api/v2', inherit_from=api_v1
)
```

##### Override routes
To override copied routes, just redeclare them.

```
@api_v1.route('/user/<user_id>/')
def username(user_id):
    username = User.query.get(user_id).username
    return jsonify(username=username)

@api_v2.route('/user/<user_id>/')
def user_info(user_id):
    username = User.query.get(user_id).username
    firstname = User.query.get(user_id).firstname
    return jsonify(data=dict(username=username, firstname=firstname))
```

##### Remap endpoints
Use the `remapping` keyword argument in the constructor to change the endpoints of inherited routes.

```
remapping = {'/users/list/': '/users/'}

api_v2 = APIBlueprint(
    'api_v2', __name__, subdomain='', url_prefix='/api/v2', inherit_from=api_v1,
    remapping=remapping
)

```

See the [docs](http://flask-apiblueprint.readthedocs.org/en/latest/) for more details or run the `app.py` file to see how the [sample_api](sample_api) is implemented.

```
$ python app.py
```
