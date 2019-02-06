import asyncio

import discord
import youtube_dl

from collections import defaultdict
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

# TODO dodac playlisty, wsparcie dla skipowania, replay, głośność, ogólna komenda
# TODO wychodzenie gdy kanal pusty, wsparcie dla innych serwisów, aktualnie grana nuta
# TODO ogarnąć jak działa YoutubeDL i jakie dane można z niego wyciągnąć
# TODO pozwolic na wybranie konkretnej nuty z listy, lirycs

ytdl_format_options = {
    'format': 'bestaudio/worst',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = { 'before_options': '-nostdin', 'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def get_results(cls, url, loop=None):
        """:returns all the results it was able to find on YT"""

        loop = loop or asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

    @classmethod
    async def get_music_stream(cls, data_url, data):
        """:returns an :FFmpegPCMAudio: object"""
        return cls(discord.FFmpegPCMAudio(data_url, **ffmpeg_options,data=data))


class VoiceEntry:

    def __init__(self, requester, requested_song_data, channel, player=None):
        self.requested_song_data = requested_song_data
        self.requester = requester
        self.channel = channel
        self.player = player

        def __str__():
            return "test"


class VoiceState:

    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()  # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            self.current.player.start()
            await self.play_next_song.wait()


class MusicModule:

    def __init__(self, bot):
        self.bot = bot
        self.query = defaultdict(list)
        self.all_entries = {}

    @commands.command()
    async def play(self, ctx, *, url):
        """"""

        async with ctx.typing():

            # fetches exactly 4 song from youtube
            results = await YTDLSource.get_results("ytsearch4:"+url, loop=self.bot.loop)

            try:
                entries = results['entries']

                # when user send this command, create a basic entry in self.query
                # and provide all the data needed for the decision
                try:
                    # see if we should append new :VoiceEntry: and do so only if given user has zero song or
                    # the last one is not set up properly ie missing song url
                    if not len(self.query[ctx.author.id]) or \
                                    self.query[ctx.author.id][-1].requested_song_url is not None:

                        self.query[ctx.author.id].append(VoiceEntry(requester=ctx.author,
                                                                    channel=None, #we will have to fix this later
                                                                    requested_song_data=entries))

                        # ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                except KeyError:
                    pass

                # if there are more entries, let the user decide which one he wants to listen to
                if len(entries) > 1:
                    await ctx.send("Choose which one you'd like to listen to\n" +
                                   await self.prepare_titles(entries) +
                                   "To select a song simply type: ``//select song_number``")
            except KeyError:
                await ctx.send("Sorry, I've found nothing")


    @commands.command()
    async def select(self, ctx, number: int):

        if not len(self.query[ctx.author.id]):
            await ctx.send(ctx.author.mention + ", you haven't requested any songs yet. \n"
                                          "To see how, just type ``//help MusicModule``")
            pass

        elif self.query[ctx.author.id][-1].player is not None:
            await ctx.send(ctx.author.mention + "You have nothing to select from. "
                                                "You can request a new song if you'd like."
                                                "\n To see how, just type ``//help MusicModule``")
        else:
            data = self.query[ctx.author.id][-1].requested_song_data
            # creates a player for later use
            self.query[ctx.author.id][-1].player = await YTDLSource.get_music_stream(
                data[number - 1]['url'],
                data[number - 1]
            )

            self.query[ctx.author.id][-1].requested_song_data = data[number - 1]

            await ctx.send(ctx.author.mention +"Your song: {s} has been added to query".
                           format(s=data[number - 1]['title']))


    @commands.command()
    async def pause(self, ctx):
        """pauses the stream"""
        print(ctx.voice_client)
        ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """resumes the stream"""
        ctx.voice_client.resume()

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def Stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.stop()

    #################################
    #            HELPERS            #
    #################################

    async def prepare_titles(self, entries):
        titles = '```css\n'

        for number, entry in enumerate(entries):
            titles += str(number + 1) + ". " + entry["title"] + "\n"

        return titles + "```"

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    print("Added MusicModule")
    #bot.add_cog(MusicModule(bot))
