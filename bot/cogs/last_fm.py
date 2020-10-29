import json
import urllib
import discord
from bot.settings import MUSIC_TOKEN
from discord.ext import commands

class MusicCog(commands.Cog):
    """
    Commands for song searching
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="getsong",
        brief="gets info about a song",
        description="takes in song by itself or song followed by artist seperated by ; ",
        aliases=['song', 'gets']
    )
    async def getsong(self, ctx, *, args):
        """Function to return discord embed with song info"""
        try:
            if ', ' in args:
                args = args.split('; ')
                data = get_track(args[0], args[1])
            else:
                data = get_track(args)
            if len(data) > 0:
                embed = discord.Embed(title=f"{data['name']} by {data['artist']['name']}", url=data['url'])
                embed.add_field(name='Artist', value=data['artist']['name'])
                embed.add_field(name='Album', value=data['album']['title'])
                embed.set_thumbnail(url=data['album']['image'][2]['#text'])
                await ctx.send(embed=embed)
            else:
                await ctx.send("Invalid Search Try Again")
        except IndexError:
            await ctx.send("Invalid search term try another")

    @commands.command(
      name="getlyrics",
      brief="a command to get song lyrics",
      description="takes in song by itself or song followed by artist seperated by ; ",
      aliases=['lyrics', 'getl']
    )
    async def get_lyrics(self, ctx, *, args):
        """Function to return discord embed with song info and lyrics"""
        try:
                if ' ; ' in args:
                    args = args.split('; ')
                    data = get_track(args[0], args[1])
                else:
                    data = get_track(args)
                track = urllib.parse.quote(data['name']).lower()
                artist = urllib.parse.quote(data['artist']['name']).lower()
                with urllib.request.urlopen('https://api.lyrics.ovh/v1/'+artist+'/'+track) as url:
                    lyrics = json.loads(url.read().decode())['lyrics']
                if not lyrics or len(lyrics) > 2048:
                    lyrics = "Lyrics couldn't be found or are unavaliable at this time"
                embed = discord.Embed(title=f"{data['name']} by {data['artist']['name']}", url=data['url'], description=lyrics)
                embed.add_field(name='Artist', value=data['artist']['name'])
                embed.add_field(name='Album', value=data['album']['title'])
                embed.set_thumbnail(url=data['album']['image'][2]['#text'])
                await ctx.send(embed=embed)
        except IndexError:
                await ctx.send('Invalid search term, try again')

    @commands.command(
      name="getalbum",
      brief="gets info about an album",
      description="takes in album by itself or album followed by artist seperated by ; ",
      aliases=['album', 'getal']
    )
    async def getalbum(self, ctx, *, args):
        """Function to return discord embed with album info"""
        try:
                if '; ' in args:
                    args = args.split('; ')
                    data = get_album(args[0], args[1])
                else:
                    data = get_album(args)
                embed = discord.Embed(title=f"{data['album']['name']} by {data['album']['artist']}", url=data['album']['url'])
                embed.add_field(name='Artist', value=data['album']['artist'])
                embed.set_thumbnail(url=data['album']['image'][2]['#text'])
                try:
                    embed.add_field(name='Release Data', value=data['album']['wiki']['published'], inline=False)
                except KeyError:
                    pass
                try:
                    embed.add_field(name='About', value=data['album']['wiki']['summary'].split('<a', 1)[0])
                except KeyError:
                    pass
                await ctx.send(embed=embed)
        except IndexError:
                await ctx.send('Invalid search term, try again')

    @commands.command(
      name="getartist",
      brief="A command that get's info about an artist",
      description="Takes in just artist name",
      aliases=['artist', 'getar']
    )
    async def getartist(self, ctx, *, args):
        """Function to return discord embed with artist info"""
        try:
                data = get_artist(args)
                album_data = get_data('artist.gettopalbums&artist='+urllib.parse.quote(data['name']))['topalbums']['album']
                bio = data['bio']['summary'].split('\n', 2)[0].split('<a', 1)[0]
                if bio == '':
                    bio = data['bio']['summary'].split('\n', 2)[1].split('<a', 1)[0]
                embed = discord.Embed(title=data['name'], url=data['url'], description=bio)
                embed.set_thumbnail(url=album_data[0]['image'][2]['#text'])
                top_albums = "\n".join([x["name"] for x in album_data[:10]])
                similar = "\n".join([x["name"] for x in data["similar"]["artist"]])
                if not similar:
                    similar = 'No Similar Artists Avaliable'
                embed.add_field(name='Top Albums', value=top_albums, inline=True)
                embed.add_field(name='Similar Artists', value=similar, inline=True)
                await ctx.send(embed=embed)
        except IndexError:
                await ctx.send('Invalid search term, try again')

    @commands.command(
      name="topsongs",
      brief="Gets a list of the top songs on the world charts",
      aliases=['songs', 'tops']
    )
    async def topsongs(self, ctx):
        """Function to return discord embed with top chart songs"""
        data = top_tracks()
        embed = discord.Embed(title='Top 10 Tracks', url='https://www.last.fm/charts')
        for count, song in enumerate(data[:10], 1):
                embed.add_field(name=str(count), value=f"{song['name']} by {song['artist']['name']}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(
      name="topartists",
      brief="Gets a list of the top artists on the world charts",
      aliases=['artists', 'topa']
    )
    async def topartists(self, ctx):
        """Function to return discord embed with top chart artists"""
        data = top_artists()
        embed = discord.Embed(title='Top 10 Artists', url='https://www.last.fm/charts')
        for count, artist in enumerate(data[:10], 1):
                embed.add_field(name=str(count), value=artist['name'], inline=False)
        await ctx.send(embed=embed)

def get_data(url_data1:str, url_data2:str=''):
    """returns the json data from the url, takes in the two pieces of a URL as outlined in the last.fm api docs"""
    return json.loads(urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method="+url_data1+"&api_key="+MUSIC_TOKEN+"&format=json"+url_data2).read().decode())


def get_album(album:str, artist:str=''):
        """returns the json data for a given album, takes in just an album or album and artist"""
        if not artist:
                album = urllib.parse.quote(album)
                data = get_data('album.search&album='+album)
                album = data['results']['albummatches']['album'][0]['name']
                artist = data['results']['albummatches']['album'][0]['artist']
                return get_album(album, artist)
        else:
                artist = urllib.parse.quote(artist)
                album = urllib.parse.quote(album)
                return get_data('album.getinfo', '&artist='+artist+'&album='+album)


def get_artist(artist:str):
    """returns the json data for a given artist, takes in artist name"""

    artist = urllib.parse.quote(artist)
    return get_data('artist.getinfo&artist='+artist)['artist']


def get_track(track:str, artist:str=''):
        """Returns info about a specific song/track takes in just a track or artist and track."""
        artist = urllib.parse.quote(artist)
        track = urllib.parse.quote(track)

        if artist:
        	return get_data('track.getinfo', '&artist='+artist+'&track='+track)['track']
        else:
          artist = get_data('track.search&track='+track)['results']['trackmatches']['track'][0]['artist']
          track = get_data('track.search&track='+track)['results']['trackmatches']['track'][0]['name']
          return get_track(track, artist)


def top_tracks():
        """Returns data of the top songs on the charts"""

        data = get_data('chart.gettoptracks')['tracks']['track']
        return [f for f in data]


def top_artists():
    """Returns data of the top artists"""
    data = get_data('chart.gettopartists')['artists']['artist']
    return [f for f in data]


def setup(bot):
    "Imports the cog"
    bot.add_cog(MusicCog(bot))


