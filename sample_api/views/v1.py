from flask import jsonify

from flask_apiblueprint import APIBlueprint
from sample_api import User, Media

api_v1 = APIBlueprint('api_v1', __name__, subdomain='', url_prefix='/api/v1')

@api_v1.route('/user/<user_id>/')
def username(user_id):
    username = User.query.get(user_id).username
    return jsonify(username=username)

@api_v1.route('/users/list/')
def users_list():
    users = User.query.all()
    usernames = [{'username': user.username} for user in users]
    return jsonify(data=usernames)

@api_v1.route('/media/<media_id>/')
def media_info(media_id):
    kind = Media.query.get(media_id).kind
    return jsonify(data=dict(kind=kind))


