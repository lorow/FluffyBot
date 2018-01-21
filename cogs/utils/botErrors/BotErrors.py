class BotErrors(object):
    def __init__(self):
        self.extra_errors = {
                'empty_query': 'I have not found anything you wanted to search for on this site, sorry \n Maybe try different tags or site?',
                'NoCommand':    'There is no such command. Try using the help command if you need some help',
                'NotNSFWChannel': 'http://i.imgur.com/cXx4arL.png',
                'NotLoliChannel': 'https://i.imgur.com/AvPnHE8.png',
                'dictNull': 'dict is null'}

    async def add_error(self, name, message):
        self.extra_errors[name] = message

    async def get_error(self, name):
        try:
            return self.extra_errors[name]
        except KeyError:
            return 'error: no such error message'

    async def get_all_errors(self):
        return self.extra_errors

    async def empty_query(self):
        return self.get_error('empty_query')

    async def NotNSFWChannel(self):
        # keep your porn of my screen
        return self.get_error('NotNSFWChannel')

    async def NotLoliChannel(self):
        return self.get_error('NotLoliChannel')

    async def NoCommand(self):
        return self.get_error('NoCommand')
