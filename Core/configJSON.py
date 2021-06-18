import ujson


class ConfigManager(object):
    def __init__(self):
        self._load_config()

    def _load_config(self):
        with open("./config.json", "r") as config:
            self.__dict__ = ujson.load(config)

    def _reload_config(self):
        self._load_config()

    def get_field(self, field):

        if field == "":
            print("you forgot something")
            quit(1)

        try:
            return self.__dict__[field]
        except KeyError as error:
            print("this field doesn't exist, check your query")
            print(error)
            quit(1)
