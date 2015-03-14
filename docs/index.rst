.. flask-apiblueprint documentation master file, created by
   sphinx-quickstart on Fri Mar 13 14:37:56 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to flask-apiblueprint's documentation!
==============================================

.. toctree::
   :maxdepth: 2

Construct an APIBlueprint
-------------------------

An ``APIBlueprint`` extends the ``flask.Blueprint <http://flask.pocoo.org/docs/0.10/blueprints/>`` class.

Provide the ``inherit_from`` parameter to the constructor to copy routes from another ``APIBlueprint``.

::

    api_v1 = APIBlueprint('api_v1', __name__, subdomain='', url_prefix='/api/v1')

    app.register(api_v1)

    api_v2 = APIBlueprint('api_v2', __name__, subdomain='', url_prefix='/api/v2', inherit_from=api_v1)

    app.register(api_v2)


That means routes get copied over so you can just do this:

::

    @api_v1.route('/user/<user_id>/')
    def username(user_id):
        username = User.query.get(user_id).username
        return jsonify(username=username)

    GET /api/v1/user/1/

        {
            "username": "gimmebear"
        }


    GET /api/v2/user/1/

        {
            "username": "gimmebear"
        }



Override routes
---------------
If you want to override a route, you just redefine it on your ``APIBlueprint``. For instance, if in the new version of your API you decide you want ``user_info`` to return a dictionary of data::

    @api_v2.route('/user/<user_id>/')
    def user_info(user_id):
    username = User.query.get(user_id).username
    firstname = User.query.get(user_id).firstname
    return jsonify(data=dict(username=username, firstname=firstname))

    GET /api/v1/user/1/

        {
            "username": "gimmebear"
        }


    GET /api/v2/user/1/
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
    'api_v2', __name__, subdomain='', url_prefix='/api/v2', inherit_from=api_v1, remapping=remapping)

    @api_v1.route('/users/list/')
    def users_list():
        users = User.query.all()
        usernames = [{'username': user.username} for user in users]
        return jsonify(data=usernames)


    GET /api/v1/users/list/

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

    GET /api/v2/users/

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


Indices and tables
==================
.. * :ref:`genindex`
* :ref:`search`

