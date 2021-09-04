import settings


class ConfigManager(object):
    @staticmethod
    def get_field(field, default=None):
        try:
            return getattr(settings, field)
        except (KeyError, AttributeError):
            return default
