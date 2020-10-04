
import discord
from discord.ext import commands
import urllib.request, json 
import urllib

api_key = '386e76f571fd03ac5e56501fe05db36a'


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def getsong(self,ctx,*,args):
      if ', ' in args:
        args=args.split(', ')
        data= get_track(args[0],args[1])
      else:
        data = get_track(args)
      if data['lyrics']['lyrics']=='':
        lyrics = 'No Lyrics Avaliable'
      else:
        lyrics = '**Lyrics:\n**'+data['lyrics']['lyrics']
      embed=discord.Embed(title=data['name'],url=data['url'],description=lyrics)
      embed.add_field(name='Artist',value=data['artist']['name'])
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MusicCog(bot))



def get_data(method,method2=''):
  with urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method="+method+"&api_key="+api_key+"&format=json"+method2) as url:
    data = json.loads(url.read().decode())
  return data


def get_album(album):
  album = urllib.parse.quote(album)
  data = get_data('album.search&album='+album)
  artist = data['results']['albummatches']['album'][0]['artist']
  artist = urllib.parse.quote(artist)
  return get_data('album.getinfo','&artist='+artist+'&album='+album)

def get_artist(artist):
  artist = urllib.parse.quote(artist)
  return get_data('artist.getinfo&artist='+artist)['artist']

def get_track(track,artist=''):
  track = urllib.parse.quote(track)
  artist = urllib.parse.quote(artist)
  
  if artist != '':
    data =  get_data('track.getinfo','&artist='+artist+'&track='+track)['track']
    track= urllib.parse.quote(data['name']).lower()
    artist=urllib.parse.quote(data['artist']['name']).lower()
        
    with urllib.request.urlopen('https://api.lyrics.ovh/v1/'+artist+'/'+track) as url:
      data['lyrics']=json.loads(url.read().decode())
    return data
  else:
    artist = get_data('track.search&track='+track)['results']['trackmatches']['track'][0]['artist']
    track = get_data('track.search&track='+track)['results']['trackmatches']['track'][0]['name']
    return get_track(track,artist)

    
def top_tracks():
  data = get_data('chart.gettoptracks')['tracks']['track']
  songs = []
  for f in data:
    songs.append(f)
  return songs
    

def top_artists():
  data = get_data('chart.gettopartists')['artists']['artist']
  artists =[]
  for f in data:
    artists.append(f)
  return artists
