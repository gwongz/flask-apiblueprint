.. flask-apiblueprint documentation master file, created by
   sphinx-quickstart on Fri Mar 13 14:37:56 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask-APIBlueprint | Read the Docs
==============================================
.. toctree::
   :maxdepth: 2

==================
Flask-APIBlueprint
==================
Flask-APIBlueprint is a Flask micro-framework extension which adds support for route inheritance for Blueprints.

Construct an APIBlueprint
-------------------------

An ``APIBlueprint`` extends the `flask.Blueprint_` class.

Providing the ``inherit_from`` parameter to the constructor copies routes from another ``APIBlueprint``.

::

    api_v1 = APIBlueprint('api_v1', __name__, subdomain='', url_prefix='/api/v1')

    app.register(api_v1)

    api_v2 = APIBlueprint(
        'api_v2', __name__,
        subdomain='',
        url_prefix='/api/v2',
        inherit_from=api_v1
    )

    app.register(api_v2)


That means you can just do this:

::

    @api_v1.route('/user/<user_id>/')
    def username(user_id):
        username = User.query.get(user_id).username
        return jsonify(username=username)

    GET /api/v1/user/1/ returns:

        {
            "username": "gimmebear"
        }


    GET /api/v2/user/1/ returns:

        {
            "username": "gimmebear"
        }



Override routes
---------------
If you want to override a route, you just redefine it on your ``APIBlueprint``. For instance, you version your API and decide you want to return a dictionary of user data instead of just a username::

    @api_v2.route('/user/<user_id>/')
    def user_info(user_id):
        username = User.query.get(user_id).username
        firstname = User.query.get(user_id).firstname
        return jsonify(data=dict(username=username, firstname=firstname))

    GET /api/v1/user/1/ returns:

        {
            "username": "gimmebear"
        }


    GET /api/v2/user/1/ returns:
        {
            "data": {
                "firstname": "Smoky",
                "username": "gimmebear"
            }
        }



Remap endpoints
---------------
You might decide that you want to change the endpoint of a particular route but not the response in a new version of your API. You can do this via the ``remapping`` keyword argument

::

    remapping = {'/users/list/': '/users/'}

    api_v2 = APIBlueprint(
        'api_v2',
         __name__,
         subdomain='',
         url_prefix='/api/v2',
         inherit_from=api_v1, remapping=remapping
    )

    @api_v1.route('/users/list/')
    def users_list():
        users = User.query.all()
        usernames = [{'username': user.username} for user in users]
        return jsonify(data=usernames)


    GET /api/v1/users/list/ returns:

        {
            "data": [
                {
                    "username": "gimmecat"
                },

                {
                    "username": "gimmebear"
                }
            ]
        }

    GET /api/v2/users/ returns:

        {
            "data": [
                {
                    "username": "gimmecat"
                },
                {
                    "username": "gimmebear"
                }
            ]
        }

.. _flask.Blueprint: http://flask.pocoo.org/docs/0.10/blueprints/
Indices and tables
==================
