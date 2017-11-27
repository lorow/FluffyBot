class checks(object):

    async def is_loli(self, channel):
        return True if "loli" in channel.name.lower() and channel.is_nsfw() else False
