class CustomRouter(object):

    def db_for_read(self, model, **hints):
        """Send all read operations on myapp app models to `test_db`."""
        if model._meta.app_label == 'myapp':
            return 'myapp'
        return 'default'

    def db_for_write(self, model, **hints):
        """Send all write operations on myapp app models to `test_db`."""
        if model._meta.app_label == 'myapp':
            return 'myapp'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two models that are both in the myapp app.
        if obj1._meta.app_label == 'myapp' and obj2._meta.app_label == 'myapp':
            return True
        # No opinion if neither object is in the myapp app (defer to default or other routers).
        elif 'myapp' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True

        # Block relationship if one object is in the myapp app and the other isn't.
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the myapp app's models get created on the right database."""
        if app_label == 'myapp':
            # The myapp app should be migrated only on the myapp_db database.
            return db == 'myapp'
        return 'default'
