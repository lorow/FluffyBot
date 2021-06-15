import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
from collections import defaultdict
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

ytdl_format_options = {
    "format": "bestaudio/worst",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": False,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": False,
    "no_warnings": False,
    "default_search": "ytsearch5",  # the amount of entries we need
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    "before_options": "-nostdin -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


ytdl = YoutubeDL(ytdl_format_options)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get("title")
        self.web_url = data.get("webpage_url")
        self.duration = data.get("duration")

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def get_entries(cls, search: str, *, loop):
        """Downloads five videos of given query or the one from the link"""
        loop = loop or asyncio.get_event_loop()
        to_run = partial(ytdl.extract_info, url=search, download=False)
        data = await loop.run_in_executor(None, to_run)

        if "entries" in data:
            data = data["entries"]

        return data

    @classmethod
    async def create_source(cls, data, ctx):
        return {
            "webpage_url": data["webpage_url"],
            "requester": ctx.author,
            "title": data["title"],
        }

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data["requester"]

        to_run = partial(ytdl.extract_info, url=data["webpage_url"], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(
            discord.FFmpegPCMAudio(
                data["url"],
                before_options=ffmpeg_options["before_options"],
                options=ffmpeg_options["options"],
            ),
            data=data,
            requester=requester,
        )


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = (
        "bot",
        "_guild",
        "_channel",
        "_cog",
        "queue",
        "next",
        "current",
        "np",
        "volume",
    )

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = 1
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                if self in self._cog.players.values():
                    return self.destroy(self._guild)
                return

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(
                        source, loop=self.bot.loop
                    )
                except Exception as e:
                    await self._channel.send(
                        f"There was an error processing your song.\n"
                    )
                    print(e)
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(
                source,
                after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set),
            )
            self.np = await self._channel.send(
                f"**Now Playing:** `{source.title} {source.duration}` requested by "
                f"`{source.requester}`"
            )
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ("bot", "players", "selectors")

    __json_doc__ = """
        {
           "ignore": false,
           "brief":"A simple music module that let's you play some good (or not) music from youtube. It supports links as well as searching.",
           "commands":{
               "join":{
                   "desc": "aliases: [connect], Command for summoning or moving the bot to a specific channel. You need to be connected to one thought",

                   "args":{
                       "channel": "The name of the channel you want the bot to join / move to"
                   }
               },
               "play":{
                   "desc": "Request a song and get it added to the queue. This command will also attempt to join your current voice channel",

                   "args":{
                       "song_name": "The name of the song you'd like to have added to the queue. You can also send a valid youtube link"
                   }
               },
               "select":{
                   "desc": "Select a song from the five the bot found on youtube",

                   "args":{
                       "index": "The number of the song you'd like to listen to."
                   }
               },
               "playlist":{
                   "desc": "asliases [queue_info, q, playlist], Shows a list of currently queued songs",

                   "args":{}
               },
               "pause":{
                   "desc": "Pauses the song",

                   "args":{}
               },
               "resume":{
                   "desc": "resumes the previously paused song",

                   "args":{}
               },
               "current":{
                   "desc": "aliases [np, current, playing], Shows some info about the current song",

                   "args":{}
               },
               "skip":{
                   "desc": "skips the current playing song",

                   "args":{}
               },
               "quit":{
                   "desc": "Rudely makes the bot leave the channel. The bot is sad now :c",

                   "args":{}
               },       
           }
       } 
       """

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.selectors = defaultdict(lambda: defaultdict(list))

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            for entry in self.players[guild.id].queue._queue:
                if isinstance(entry, YTDLSource):
                    entry.cleanup()
            self.players[guild.id].queue._queue.clear()
        except KeyError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(
                    "This command can not be used in Private Messages."
                )
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send(
                "Error connecting to Voice Channel. "
                "Please make sure you are in a valid channel or provide me with one"
            )

        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    async def cleanup_selections(self, ctx):
        """cleans up the selection queue"""
        # if this user in this guild has something left, pop it
        if self.selectors[ctx.guild.id][ctx.author.id]:
            self.selectors[ctx.guild.id][ctx.author.id].pop(-1)

        # else, pop this user from the selection queue
        if not self.selectors[ctx.guild.id][ctx.author.id]:
            del self.selectors[ctx.guild.id][ctx.author.id]

        # if this guild is empty, pop it too
        if not self.selectors[ctx.guild.id]:
            del self.selectors[ctx.guild.id]

    async def prepare_options(self, entries):
        prep_entries = []

        if type(entries) is list:
            for number, entry in enumerate(entries):
                prep_entries.append(str(number + 1) + ". " + entry["title"])

            return "\n".join(prep_entries)
        else:
            return "\n" + f"1. {entries['title']}"

    async def print_entries(self, entries, ctx):
        embed = discord.Embed()
        options = await self.prepare_options(entries)
        embed.add_field(
            name=f"@{ctx.author}, here's what I've found:",
            value=f"```css\n{options}```",
        )
        embed.add_field(
            name="Here's how to use:", value="//select [number you wish to be played]"
        )

        await ctx.send(embed=embed)

    async def put_on_queue(self, ctx, data):
        player = self.get_player(ctx)
        source = await YTDLSource.create_source(data=data, ctx=ctx)
        await player.queue.put(source)

    @commands.command(name="connect", aliases=["join"])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        """Connect to voice."""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel(
                    "No channel to join. Please either specify a valid channel or join one."
                )

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f"Moving to channel: <{channel}> timed out.")
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    f"Connecting to channel: <{channel}> timed out."
                )

        await ctx.send(f"Connected to: **{channel}**")

    @commands.command(name="play", aliases=["sing"])
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            try:
                await ctx.invoke(self.connect_)
            except Exception as e:
                print(e)
                await ctx.send("Something went wrong, please try again")

        entries = await YTDLSource.get_entries(search, loop=self.bot.loop)
        # if we get a single entry, put it right away on the queue, else let the user choose
        if type(entries) is dict:
            await self.put_on_queue(ctx, entries)
            await ctx.send(f"{entries['title']} added to the queue!")
        else:
            await self.print_entries(entries, ctx)

            self.selectors[ctx.guild.id][ctx.author.id].append(entries)

    @commands.command()
    async def select(self, ctx, selection: int):

        if ctx.author.id not in self.selectors[ctx.guild.id]:
            return await ctx.send(f"@{ctx.author}, you have nothing to select from")

        data = self.selectors[ctx.guild.id][ctx.author.id][-1][selection - 1]
        await self.put_on_queue(ctx, data)

        await ctx.send(
            f"Added {self.selectors[ctx.guild.id][ctx.author.id][-1][selection - 1]['title']}"
        )
        await self.cleanup_selections(ctx)

    @commands.command(name="pause")
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send("I am not currently playing anything!")
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f"**`@{ctx.author}`**: Paused the song.")

    @commands.command(name="resume")
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("Nothing is currently being played")
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f"**`@{ctx.author}`**: Resumed the song.")

    @commands.command(name="skip")
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("Nothing is currently being played")

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f"**`{ctx.author}`**: Skipped the song")

    @commands.command(name="queue", aliases=["q", "playlist"])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("I am not currently connected to voice!")

        player = self.get_player(ctx)

        print(player.current)

        if player.queue.empty() and player.current is None:
            return await ctx.send("There are currently no more queued songs.")

        # Grab up to 5 entries from the queue and the current one...
        current = player.current
        upcoming = [current] + list(itertools.islice(player.queue._queue, 0, 5))

        fmt = "\n".join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f"Upcoming - Next {len(upcoming)}", description=fmt)

        await ctx.send(embed=embed)

    @commands.command(
        name="now_playing", aliases=["np", "current", "currentsong", "playing"]
    )
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("Nothing is currently being played")

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send("Nothing is currently being played")

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(
            f"**Now Playing:** `{vc.source.title}` "
            f"requested by `{vc.source.requester}`."
        )

    @commands.command(name="volume", aliases=["vol"])
    async def change_volume(self, ctx, *, vol: float):
        """
        Change the player volume.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("I am not currently connected to voice!")

        if not 0 < vol < 101:
            return await ctx.send("Please enter a value between 1 and 100.")

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f"**`{ctx.author}`**: Set the volume to **{vol}%**")

    @commands.command(name="quit")
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("Nothing is currently being played")

        await self.cleanup(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))
