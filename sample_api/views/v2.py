from flask import jsonify

from flask_apiblueprint import APIBlueprint

from sample_api import User, Media
from sample_api.views.v1 import api_v1

remapping = {'/users/list/': '/users/'}

api_v2 = APIBlueprint('api_v2', __name__, subdomain='', url_prefix='/api/v2', inherit_from=api_v1, remapping=remapping)

@api_v2.route('/user/<user_id>/')
def user_info(user_id):
    username = User.query.get(user_id).username
    firstname = User.query.get(user_id).firstname
    return jsonify(data=dict(username=username, firstname=firstname))