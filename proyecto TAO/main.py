# bot.py

import discord
import fortniteapi
import aiohttp
import pymongo
from fortnitepy.client import Client

cluster = pymongo.MongoClient("mongodb+srv://<discordsyntax0>:<S1l3ntxv>@<cluster>.mongodb.net/test")
db = cluster["fortnite"]
users = db["users"]

client = discord.Client()
fortnite_client = Client()

@client.event
async def on_ready():
  print('Bot listo!')

@client.event
async def on_message(message):

  if message.content.startswith('!login'):
  
    username = message.content.split()[1] 
    password = message.content.split()[2]

    await fortnite_client.login(username, password)

    user = {
      "discord_id": message.author.id,
      "fortnite_username": username
    }
    
    users.insert_one(user)
    await message.channel.send('Login exitoso!')

  if message.content.startswith('!logout'):
  
    user = users.find_one({"discord_id": message.author.id})
    await fortnite_client.logout()
    users.delete_one(user)
    await message.channel.send('Logout exitoso!')

  if message.content.startswith('!misiones'):
    
    user = users.find_one({"discord_id": message.author.id})   
    fortnite_client.user = user
    
    await message.channel.send('Obteniendo misiones diarias...')
    
    api = fortniteapi.FortniteAPI()
    data = api.get_daily_missions()
    
    embed = discord.Embed(title='Misiones Diarias')
    for mission in data:
      embed.add_field(name=mission['name'], value=mission['description'])
      
    await message.channel.send(embed=embed)

  if message.content.startswith('!locker'):
  
    user = users.find_one({"discord_id": message.author.id})
    fortnite_client.user = user
    
    await message.channel.send("Obteniendo skins...")
    
    locker_data = await fortnite_client.locker.get_locker()
    
    skin_ids = [item.id for item in locker_data.outfits]
    
    async with aiohttp.ClientSession() as session:
      skin_urls = []
      for skin_id in skin_ids:
        url = f"https://skindb.co/api/v1/images/fortnite/outfits/{skin_id}"
        response = await session.get(url)
        data = await response.json()
        skin_urls.append(data.get("data", {}).get("images", {}).get("icon"))
        
    embed = discord.Embed(title=f"{message.author.display_name}'s Locker")
    for skin_url in skin_urls:
      embed.set_image(url=skin_url)
      await message.channel.send(embed=embed)

client.run('MTE1ODIwMTQwNzg1MDE1MTkzNg.G5NyaZ.zA9qBgm9rBD09LmeOqiAYseY2Gh3R5a3UCV8Iw')