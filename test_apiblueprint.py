import unittest

from mock import patch, call
from flask import Flask
from flask.ext.testing import TestCase

from flask_apiblueprint import APIBlueprint

class BaseTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.initialize()

    def initialize(self):
        pass

class TestAPIBlueprint(BaseTest):
    # def initialize(self, *args, **kwargs):
        # super(TestAPIBlueprint, self).initialize(*args, **kwargs)

    def _setup_parent_blueprint(self):
        bp = APIBlueprint('bp_v1', __name__, url_prefix='/v1')

        @bp.route('/foo')
        def foo():
            return 'Foo'

        @bp.route('/bar')
        def bar():
            return 'Bar'

        return bp, foo, bar

    @patch.object(APIBlueprint, 'copy_routes')
    def test_setup_no_inheritance(self, copy_routes):
        bp = APIBlueprint('bp', __name__)
        self.assertFalse(copy_routes.called)

    @patch.object(APIBlueprint, 'copy_routes')
    def test_setup_with_inheritance(self, copy_routes):
        """
        Verify that copy routes is called when a blueprint is initialized
        with an `inherit_from` argument.
        """
        bp = APIBlueprint('bp', __name__)
        inherited_bp = APIBlueprint('bp_v2', __name__, url_prefix='/v2', inherit_from=bp)
        copy_routes.assert_called_once_with(remapping=None)

    @patch.object(APIBlueprint, 'route')
    def test_route(self, route):
        """
        Verify that route is called with right arguments when a blueprint is
        inherited and then overloaded.
        """
        bp, foo, bar = self._setup_parent_blueprint()
        inherited_bp = APIBlueprint('bp_v2', __name__, url_prefix='/v2', inherit_from=bp)

        @inherited_bp.route('/bar')
        def overloaded_bar():
            return 'Overloaded bar'

        expected_calls = [call('/foo'), call('/bar'), call('/bar')]
        self.assertEqual(route.call_args_list, expected_calls)

    @patch.object(APIBlueprint, 'add_url_rule')
    def test_add_url_rule(self, add_url_rule):
        """
        Verify that add_url_rule is called with the right arguments when a route is
        inherited and then overloaded.
        """
        bp, foo, bar = self._setup_parent_blueprint()
        inherited_bp = APIBlueprint('bp_v2', __name__, url_prefix='/v2', inherit_from=bp)

        @inherited_bp.route('/bar')
        def overloaded_bar():
            return 'Overloaded bar'

        expected_calls = [
            call('/foo', 'foo', foo),
            call('/bar', 'bar', bar),
            call('/bar', 'overloaded_bar', overloaded_bar)
        ]
        self.assertEqual(expected_calls, add_url_rule.call_args_list)

    @patch.object(APIBlueprint, 'record')
    def test_record_not_inherited_route(self, record):
        """
        Verify that record is called with right arguments when a route is added.
        """
        bp = APIBlueprint('bp_v1', __name__, url_prefix='/v1')

        @bp.route('/foo')
        def foo():
            return 'Foo'

        self.assertEqual(record.call_count, 1)
        expected_call = record.call_args_list[0]
        call_args, call_kwargs = expected_call[0], expected_call[1]
        self.assertEqual(call_kwargs, dict(rule='/foo'))

class TestAPIBlueprintIntegration(TestAPIBlueprint):
    def initialize(self, *args, **kwargs):
        super(TestAPIBlueprintIntegration, self).initialize(*args, **kwargs)
        self.bp, self.foo, self.bar = self._setup_parent_blueprint()
        self.app.register_blueprint(self.bp)

    def test_overloaded_routes(self):
        inherited_bp = APIBlueprint('bp_v2', __name__, url_prefix='/v2', inherit_from=self.bp)

        @inherited_bp.route('/bar')
        def overloaded_bar():
            return 'Overloaded Bar'

        self.app.register_blueprint(inherited_bp)
        self.assertEqual(self.client.get('/v2/foo').data, self.client.get('v1/foo').data)
        self.assertEqual(self.client.get('/v2/bar').data, 'Overloaded Bar')
        self.assertEqual(self.client.get('/v1/bar').data, 'Bar')

    def test_inherited_routes(self):
        inherited_bp = APIBlueprint('bp_v2', __name__, url_prefix='/v2', inherit_from=self.bp)
        self.app.register_blueprint(inherited_bp)
        self.assertEqual(self.client.get('/v2/foo').data, self.client.get('v1/foo').data)
        self.assertEqual(self.client.get('/v2/bar').data, self.client.get('v1/bar').data)

    def test_remapped_routes(self):
        inherited_bp = APIBlueprint(
            'bp_v2',
            __name__,
            url_prefix='/v2',
            inherit_from=self.bp,
            remapping={
                '/foo': '/faz',
            }
        )

        self.app.register_blueprint(inherited_bp)

        self.assertEqual(self.client.get('/v2/foo').status_code, 404)
        self.assertEqual(self.client.get('/v2/faz').data, self.client.get('/v1/foo').data)
        self.assertEqual(self.client.get('/v2/bar').data, self.client.get('/v1/bar').data)

if __name__ == '__main__':
    unittest.main()