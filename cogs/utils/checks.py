class checks(object):
    # note to self, convert this to decorators
    async def is_loli(self, channel):
        return True if "loli" in channel.name.lower() and channel.is_nsfw() else False
