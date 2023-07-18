import os
import discord
from discord.ext import commands,tasks
import requests
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime

import config

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix="!", intents=intents)

async def status_task():
    while True:
        r = requests.post('https://api.mir4global.com/wallet/prices/draco/lastest', json={"key": "value"})
        draco = r.json()['Data']['USDDracoRate'] 
        dracoeski = draco[0:6]
        dracousd = float(dracoeski.replace(',', '').replace('%', ''))
        URL = "https://bigpara.hurriyet.com.tr/doviz/dolar/"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib') 
        dolareski= soup.find('span', attrs = {'class':'value up'}).text
        dolar = float(dolareski.replace(',', '.'))
        dracotl = float(dracousd)*float(dolar)
        await client.change_presence(activity=discord.Game(name="₺"+"{:.2f}".format(dracotl)+" | "+"$"+str(dracousd)))
  
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print("{:.2f}".format(dracotl)+"-----"+str(dracousd)+"-----"+time)
        
        await asyncio.sleep(5)
      
        r2 = requests.post('https://api.mir4global.com/wallet/prices/derby', json={"key":"value"})
        uzunluk= len(r2.json()['Data'])-1
        ds = r2.json()['Data'][uzunluk]['DS']
        derbyds = r2.json()['Data'][uzunluk]['SmeltingCost']
        gunlukds = int(ds)+int(derbyds)

        await client.change_presence(activity=discord.Game(name=str(gunlukds)+" Darksteel"))

        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print(str(gunlukds)+" Darksteel"+"-----"+time)
      
        await asyncio.sleep(5)


@client.event
async def on_ready():
  print('{0.user} olarak giriş yapıldı!'.format(client))
  client.loop.create_task(status_task())
  



client.run(config.botapi_key)


