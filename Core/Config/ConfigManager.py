import settings


class ConfigManager(object):

    @staticmethod
    def get_field(field):
        try:
            return getattr(settings, field)
        except KeyError as error:
            print("this field doesn't exist, check your query")
            print(error)
            quit(1)
