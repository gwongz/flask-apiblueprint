import six
import pytest

from flask import Flask
from flask_apiblueprint import APIBlueprint


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def v1_blueprint(app):
    blueprint = APIBlueprint('v1', __name__, url_prefix='/v1')

    @blueprint.route('/foo')
    def foo():
        return 'Foo'

    return blueprint


def test_blueprint_with_no_inheritance(app, v1_blueprint):
    """
    Verify route is registered as usual when a blueprint is not initialized
    with an `inherit_from` arg.
    """
    app.register_blueprint(v1_blueprint)
    response = app.test_client().get('/v1/foo')
    assert response.data == six.b('Foo')


def test_blueprint_with_inheritance(app, v1_blueprint):
    """
    Verify that parent blueprint routes are copied when a blueprint is
    initialized with an `inherit_from` argument.
    """
    inherited = APIBlueprint(
        'v2', __name__, url_prefix='/v2', inherit_from=v1_blueprint
    )
    app.register_blueprint(v1_blueprint)
    app.register_blueprint(inherited)
    v1_response = app.test_client().get('/v1/foo')
    assert v1_response.data == six.b('Foo')
    v2_response = app.test_client().get('/v2/foo')
    assert v2_response.data == v1_response.data


def test_overloaded_route(app, v1_blueprint):
    """
    Verify that an inherited blueprint can overload its routes..
    """
    inherited = APIBlueprint(
        'v2', __name__, url_prefix='/v2', inherit_from=v1_blueprint
    )

    @inherited.route('/foo')
    def overloaded_foo():
        return 'Overloaded Foo'

    app.register_blueprint(v1_blueprint)
    app.register_blueprint(inherited)
    v1_response = app.test_client().get('/v1/foo')
    assert v1_response.data == six.b('Foo')
    v2_response = app.test_client().get('/v2/foo')
    assert v2_response.data == six.b('Overloaded Foo')


def test_remapped_routes(app, v1_blueprint):
    inherited = APIBlueprint(
        'v2',
        __name__,
        url_prefix='/v2',
        inherit_from=v1_blueprint,
        remapping={'/foo': '/faz'}
    )

    app.register_blueprint(v1_blueprint)
    app.register_blueprint(inherited)

    v1_response = app.test_client().get('/v1/foo')
    assert v1_response.data == six.b('Foo')

    v2_response = app.test_client().get('/v2/foo')
    assert v2_response.status_code == 404

    v2_remapped_response = app.test_client().get('/v2/faz')
    assert v2_remapped_response.data == v1_response.data


def test_deprecated_routes(app, v1_blueprint):
    inherited = APIBlueprint(
        'v2',
        __name__,
        url_prefix='/v2',
        inherit_from=v1_blueprint,
        remapping={'/foo': None}
    )
    app.register_blueprint(inherited)
    app.register_blueprint(v1_blueprint)
    v1_response = app.test_client().get('v1/foo')
    assert v1_response.data == six.b('Foo')
    deprecated_response = app.test_client().get('v2/foo')
    assert deprecated_response.status_code == 404


def test_same_rule_can_be_registered_with_different_methods(app):
    blueprint = APIBlueprint('blueprint', __name__)

    @blueprint.route('/foo', methods=['GET'])
    def foo():
        return 'Foo'

    @blueprint.route('/foo', methods=['POST'])
    def foo_post():
        return 'Foo POST'

    app.register_blueprint(blueprint)
    get_response = app.test_client().get('/foo')
    assert get_response.data == six.b('Foo')
    post_response = app.test_client().post('/foo')
    assert post_response.data == six.b('Foo POST')
