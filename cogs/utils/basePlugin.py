class Plugin(object):
    """A base class for all plugins, it provides some useful stuff"""

    def __init__(self, permission_manager = 'test', database_manager = 'test2'):
        self.permission_manager = permission_manager
        self.database_manager = database_manager