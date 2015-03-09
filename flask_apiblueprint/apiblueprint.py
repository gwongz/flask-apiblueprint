"""
    Flask-ApiBlueprint
    ------------
    Provides route inheritance for Flask Blueprints.
    :copyright: (c) 2015 by Grace Wong.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint

class APIBlueprint(Blueprint):
    class InheritanceError(Exception): pass

    def __init__(self, *args, **kwargs):
        self.routes_to_views_map = {}
        self.inherit_from = kwargs.pop('inherit_from', None)
        remapping = kwargs.pop('remapping', None)

        super(APIBlueprint, self).__init__(*args, **kwargs)
        self.deferred_functions = {}
        if self.inherit_from:
            self.copy_routes(remapping=remapping)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """
        Customizes the behavior of :meth:`~flask.blueprints.Blueprint.add_url_rule.
        Captures and keeps track of which view functions should be mapped to
        parent routes when blueprints are inherited.
        """
        self.routes_to_views_map[rule] = dict(view_func=view_func, options=options)

        if endpoint:
            assert '.' not in endpoint, "Blueprint endpoints should not contain dots"
        self.record(lambda s:
            s.add_url_rule(rule, endpoint, view_func, **options), rule=rule)

    def record(self, func, rule=None):
        """
        Customizes the behavior of :meth:`~flask.blueprints.Blueprint.record
        so that anonymous deferred functions are mapped to a key. This way,
        redeclared functions are removed.
        """
        if self._got_registered_once and self.warn_on_modifications:
            from warnings import warn
            warn(Warning('The blueprint was already registered once '
                         'but is getting modified now.  These changes '
                         'will not show up.'))
        if not rule:
            # still need to associate it with a key for the deferred map
            rule = func
        self.deferred_functions[rule] = func

    def register(self, app, options, first_registration=False):
        """
        Customizes the behavior of :meth:`~flask.blueprints.Blueprint.register
        since `attr:deferred_functions` has been customized to now be an array
        of dictionaries instead of array of functions.

        Called by :meth:`Flask.register_blueprint` to register a blueprint
        on the application.
        """
        self._got_registered_once = True
        state = self.make_setup_state(app, options, first_registration)
        if self.has_static_folder:
            state.add_url_rule(self.static_url_path + '/<path:filename>',
                               view_func=self.send_static_file,
                               endpoint='static')

        for rule, deferred in self.deferred_functions.iteritems():
            deferred(state)

    def copy_routes(self, remapping=None):
        """
        If a Blueprint inherits from another, copy over all of the parent's
        routes.
        """
        if not self.inherit_from:
            raise APIBlueprint.InheritanceError(
                'Blueprint not properly configured to inherit routes'
            )

        parent_blueprint = self.inherit_from
        for rule, view_info in parent_blueprint.routes_to_views_map.iteritems():
            view_func = view_info.get('view_func')
            options_dict = view_info.get('options')

            if remapping and remapping.get(rule):
                rule = remapping.get(rule)

            self.add_url_rule(rule, view_func=view_func, **options_dict)

