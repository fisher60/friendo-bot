import disnake
import urllib
import aiohttp
from disnake.ext import commands
from bot.settings import MUSIC_TOKEN


class Music(commands.Cog):
    """Commands for song searching."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="getsong",
        brief="a command to get song lyrics and info",
        description="takes in song by itself or song followed by artist seperated by ; ",
        aliases=['song', 'gets', 'getlyrics', 'getl']
    )
    async def get_lyrics(self, ctx: commands.Context, *, song_title: str) -> None:
        """Function to return discord embed with song info and lyrics."""
        try:
            if ';' in song_title:
                song_title = song_title.split('; ')
                data = await get_track(song_title[0], song_title[1])
            else:
                data = await get_track(song_title)
            track = urllib.parse.quote(data['name']).lower()
            artist = urllib.parse.quote(data['artist']['name']).lower()

            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.lyrics.ovh/v1/'+artist+'/'+track) as resp:
                    lyrics = (await resp.json())['lyrics']

            split_lyrics = lyrics.split('\n\n\n')
            lyric_array = [""]
            count = 0
            for f in split_lyrics:
                if len(lyric_array[count] + f) <= 256:
                    lyric_array[count] += f
                else:
                    count += 1
                    lyric_array.append(f)

            embed = disnake.Embed(title=f"{data['name']} by {data['artist']['name']}", url=data['url'])
            embed.add_field(name='Artist', value=data['artist']['name'])
            embed.add_field(name='Album', value=data['album']['title'])
            for f in lyric_array:
                if f:
                    embed.add_field(name="\u200b", value=f, inline=False)
            embed.set_thumbnail(url=data['album']['image'][2]['#text'])
            await ctx.send(embed=embed)
        except KeyError:
            embed = disnake.Embed(title="Music Cog", color=disnake.Colour.blue())
            embed.add_field(name="Error", value=f"Could not find song with title {song_title}")
            await ctx.send(embed=embed)

    @commands.command(
        name="getalbum",
        brief="gets info about an album",
        description="takes in album by itself or album followed by artist seperated by ; ",
        aliases=['album', 'getal']
    )
    async def getalbum(self, ctx: commands.Context, *, album_title: str) -> None:
        """Function to return discord embed with album info."""
        try:
            if '; ' in album_title:
                album_title = album_title.split('; ')
                data = await get_album(album_title[0], album_title[1])
            else:
                data = await get_album(album_title)

            title = f"{data['album']['name']} by {data['album']['artist']}"
            embed = disnake.Embed(title=title, url=data['album']['url'])
            embed.add_field(name='Artist', value=data['album']['artist'])
            embed.set_thumbnail(url=data['album']['image'][2]['#text'])

            wiki = data['album']['wiki']

            if "published" in wiki.keys():
                embed.add_field(name='Release Data', value=wiki["published"], inline=False)
            else:
                embed.add_field(name='About', value=wiki.split('<a', 1)[0])
            await ctx.send(embed=embed)

        except (KeyError, IndexError):
            embed = disnake.Embed(title="Music Cog", color=disnake.Colour.blue())
            embed.add_field(name="Error", value=f"Could not find album with title {album_title}")
            await ctx.send(embed=embed)

    @commands.command(
        name="getartist",
        brief="A command that get's info about an artist",
        description="Takes in just artist name",
        aliases=['artist', 'getar']
    )
    async def getartist(self, ctx: commands.Context, *, args: str) -> None:
        """Function to return discord embed with artist info."""
        try:
            data = await get_artist(args)
            start_data = await get_data('artist.gettopalbums&artist=' + urllib.parse.quote(data['name']))
            album_data = start_data['topalbums']['album']
            bio = data['bio']['summary'].split('\n', 2)[0].split('<a', 1)[0]
            if bio == '':
                bio = data['bio']['summary'].split('\n', 2)[1].split('<a', 1)[0]
            embed = disnake.Embed(title=data['name'], url=data['url'], description=bio)
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
    async def topsongs(self, ctx: commands.Context) -> None:
        """Function to return discord embed with top chart songs."""
        data = await top_tracks()
        em = disnake.Embed(title='Top 10 Tracks', url='https://www.last.fm/charts')
        for count, song in enumerate(data[:10], 1):
            em.add_field(name=str(count), value=f"{song['name']} by {song['artist']['name']}", inline=False)
        await ctx.send(embed=em)

    @commands.command(
        name="topartists",
        brief="Gets a list of the top artists on the world charts",
        aliases=['artists', 'topa']
    )
    async def topartists(self, ctx: commands.Context) -> None:
        """Function to return discord embed with top chart artists."""
        data = await top_artists()
        embed = disnake.Embed(title='Top 10 Artists', url='https://www.last.fm/charts')
        for count, artist in enumerate(data[:10], 1):
            embed.add_field(name=str(count), value=artist['name'], inline=False)
        await ctx.send(embed=embed)


async def get_data(url_data1: str, url_data2: str = '') -> dict:
    """Returns the json data from the url, takes in the two pieces of a URL from Last.FM API Docs."""
    async with aiohttp.ClientSession() as session:
        url = 'http://ws.audioscrobbler.com/2.0/?method='
        async with session.get(f"{url}{url_data1}&api_key={MUSIC_TOKEN}&format=json{url_data2}") as resp:
            data = await resp.json()
    return data


async def get_album(album: str, artist: str = '') -> dict:
    """Returns the json data for a given album, takes in just an album or album and artist."""
    if not artist:
        album = urllib.parse.quote(album)
        data = (await get_data('album.search&album='+album))
        album = data['results']['albummatches']['album'][0]['name']
        artist = data['results']['albummatches']['album'][0]['artist']
        return await get_album(album, artist)
    else:
        artist = urllib.parse.quote(artist)
        album = urllib.parse.quote(album)
        return await get_data('album.getinfo', '&artist='+artist+'&album='+album)


async def get_artist(artist: str) -> dict:
    """Returns the json data for a given artist, takes in artist name."""
    artist = urllib.parse.quote(artist)
    return (await get_data('artist.getinfo&artist='+artist))['artist']


async def get_track(track: str, artist: str = '') -> dict:
    """Returns info about a specific song/track takes in just a track or artist and track."""
    artist = urllib.parse.quote(artist)
    track = urllib.parse.quote(track)

    if artist:
        return (await get_data('track.getinfo', '&artist='+artist+'&track='+track))['track']
    else:
        artist = (await get_data('track.search&track='+track))['results']['trackmatches']['track'][0]
        track = (await get_data('track.search&track='+track))['results']['trackmatches']['track'][0]
        return await get_track(track['name'], artist['artist'])


async def top_tracks() -> list:
    """Returns data of the top songs on the charts."""
    data = (await get_data('chart.gettoptracks'))['tracks']['track']
    return [f for f in data]


async def top_artists() -> list:
    """Returns data of the top artists."""
    data = (await get_data('chart.gettopartists'))['artists']['artist']
    return [f for f in data]


def setup(bot: commands.Bot) -> None:
    """Imports the cog."""
    bot.add_cog(Music(bot))
