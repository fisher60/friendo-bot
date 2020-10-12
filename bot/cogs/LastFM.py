"""Commands for the song search module"""
import discord
import urllib
import json
from discord.ext import commands
from bot.settings import MUSIC_TOKEN

class MusicCog(commands.Cog):
    """
    Commands for song searching
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name ="getsong",
        brief ="gets info about a song"
    )
    async def getsong(self,ctx,*,args):
      try:
        if ', ' in args:
          args = args.split(', ')
          data = get_track(args[0],args[1])

        else:
            data = get_track(args)
        if len(data)>0:
            embed = discord.Embed(title=f"{data['name']} by {data['artist']['name']}", url=data['url'])
            embed.add_field(name='Artist',value=data['artist']['name'])
            embed.add_field(name='Album',value=data['album']['title'])
            embed.set_thumbnail(url=data['album']['image'][2]['#text'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid Search Try Again")
      except IndexError:
        await ctx.send("Invalid search term try another")
   

    @commands.command(
      name="getlyrics",
      brief="a command to get song lyrics"
    )
    async def get_lyrics(self,ctx,*,args):
      try:
        if ', ' in args:
          args = args.split(', ')
          data = get_track(args[0],args[1])
        else:
          data = get_track(args)
        track = urllib.parse.quote(data['name']).lower()
        artist = urllib.parse.quote(data['artist']['name']).lower()    
        with urllib.request.urlopen('https://api.lyrics.ovh/v1/'+artist+'/'+track) as url:
          lyrics = json.loads(url.read().decode())['lyrics']
        if not lyrics:
          lyrics = "Lyrics couldn't be found or are unavaliable at this time"
        embed=discord.Embed(title=f"{data['name']} by {data['artist']['name']}",url = data['url'],description=lyrics)
        embed.add_field(name='Artist',value=data['artist']['name'])
        embed.add_field(name='Album',value=data['album']['title'])
        embed.set_thumbnail(url=data['album']['image'][2]['#text'])
        await ctx.send(embed=embed)
      except IndexError:
        await ctx.send('Invalid search term, try again')

    @commands.command(
      name="getalbum",
      brief="a command to get info about a album, takes in an album name or album name and artist, formatting for the second is album name, artist with a comma seperating the two"
    )
    async def getalbum(self,ctx,*,args):
      try:
        if ', ' in args:
          args = args.split(', ')
          data = get_album(args[0],args[1])
        else:
          data = get_album(args)
        embed = discord.Embed(title=f"{data['album']['name']} by {data['album']['artist']}",url=data['album']['url'])
        embed.add_field(name='Artist',value=data['album']['artist'])
        embed.set_thumbnail(url=data['album']['image'][2]['#text'])
        try:
          embed.add_field(name='Release Data',value=data['album']['wiki']['published'],inline=False)
        except IndexError:
          pass
        try:
          embed.add_field(name='About',value=data['album']['wiki']['summary'].split('<a',1)[0])
        except IndexError:
          pass
        await ctx.send(embed=embed)
      except IndexError:
        await ctx.send('Invalid search term, try again')
      
    @commands.command(
      name="getartist",
      brief="A command that get's info about an artist, takes in an artist name"
    )
    async def getartist(self,ctx,*,args):
      try:
        data = get_artist(args)
        album_data = get_data('artist.gettopalbums&artist='+urllib.parse.quote(data['name']))['topalbums']['album']
        bio = data['bio']['summary'].split('\n',2)[0].split('<a',1)[0]
        if bio == '':
          bio = data['bio']['summary'].split('\n',2)[1].split('<a',1)[0]
        embed = discord.Embed(title=data['name'],url=data['url'],description=bio)
        embed.set_thumbnail(url=album_data[0]['image'][2]['#text'])
        similar = ''
        top_albums=''
        for f in album_data[:10]:
          top_albums=top_albums+f['name']+'\n'
        for f in data['similar']['artist']:
          similar = similar+f['name']+'\n'
        embed.add_field(name='Top Albums',value=top_albums,inline=True)
        embed.add_field(name='Similar Artists',value=similar,inline=True)
        await ctx.send(embed=embed)
      except IndexError:
        await ctx.send('Invalid search term, try again')

    @commands.command(
      name="topsongs",
      brief="Gets a list of the top songs on the world charts, this command doesn't require any args"
    )
    async def topsongs(self,ctx):
      data = top_tracks()
      embed = discord.Embed(title='Top 10 Tracks',url ='https://www.last.fm/charts')
      count = 1
      for f in data[:10]:
        embed.add_field(name=count,value=f['name']+' by '+f['artist']['name'],inline=False)
        count+=1
      await ctx.send(embed=embed)
    
    @commands.command(
      name = "topartists",
      brief = "Gets a list of the top artists on the world charts, this command doesn't require any args"
    )
    async def topartists(self,ctx):
      data = top_artists()
      embed = discord.Embed(title='Top 10 Artists',url = 'https://www.last.fm/charts')
      count = 1
      for f in data[:10]:
        embed.add_field(name=count,value=f['name'],inline=False)
        count += 1
      await ctx.send(embed=embed)


def setup(bot):
    "Imports the cog"
    bot.add_cog(MusicCog(bot))



def get_data(method,method2=''):
  """returns the json data from the url, takes in the two pieces of a URL as outlined in the last.fm api docs"""

  return json.loads(urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method="+method+"&api_key="+MUSIC_TOKEN+"&format=json"+method2).read().decode())


def get_album(album,artist=''):
  """returns the json data for a given album, takes in just an album or album and artist"""

  if artist:
    album = urllib.parse.quote(album)
    data = get_data('album.search&album='+album)
    album = data['results']['albummatches']['album'][0]['name']
    artist = data['results']['albummatches']['album'][0]['artist']
    return get_album(album,artist)
  else:
    artist = urllib.parse.quote(artist)
    album = urllib.parse.quote(album)
    return get_data('album.getinfo','&artist='+artist+'&album='+album)


def get_artist(artist):
  """returns the json data for a given artist, takes in artist name"""

  artist = urllib.parse.quote(artist)
  return get_data('artist.getinfo&artist='+artist)['artist']


def get_track(track,artist=''):
  """returns info about  a specific song/track takes in just a track or artist and track"""

  artist = urllib.parse.quote(artist)
  track =  urllib.parse.quote(track)
  
  if artist:
    data =  get_data('track.getinfo','&artist='+artist+'&track='+track)['track']
    return data
  else:
    artist = get_data('track.search&track='+track)['results']['trackmatches']['track'][0]['artist']
    track = get_data('track.search&track='+track)['results']['trackmatches']['track'][0]['name']
    return get_track(track,artist)

    
def top_tracks():
  """returns data of the top songs on the charts, requires no args"""

  output = []
  for x in range(10):
    output.append(x * 2)

  output = [x * 2 for x in range(10)]

  data = get_data('chart.gettoptracks')['tracks']['track']
  songs = [f for f in data]
  return songs
    

def top_artists():
  """returns data of the top artists takes in no args"""

  data = get_data('chart.gettopartists')['artists']['artist']
  artists =[f for f in data]

  return artists
