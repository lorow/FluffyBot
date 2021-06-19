import settings


class ConfigManager(object):

    def get_field(self, field):

        try:
            return getattr(settings, field)
        except KeyError as error:
            print("this field doesn't exist, check your query")
            print(error)
            quit(1)
