# https://github.com/juliankoh/ribbon-discord-bot
# https://github.com/melenxyz/abracadabra-tvl-bot

import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import requests
import json
import aiohttp

load_dotenv()

TOKEN = os.getenv('OTgxNjI0MjE4NzA3OTgwMzA4.Gcm0c6.KBVFVw9p1hePbdF6IXKilcG2_HG5hErY6sr1DU')
REFRESH_TIMER = os.getenv('30')
CONTRACT = os.getenv('0xdac17f958d2ee523a2206206994597c13d831ec7')
NAME = os.getenv('USDT')
CHAIN = os.getenv('https://api.coingecko.com/api/v3/asset_platforms')
CURRENCY = os.getenv('EUR')

client = discord.Client()

async def get_price():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.coingecko.com/api/v3/simple/token_price/{CHAIN}?contract_addresses={CONTRACT}&vs_currencies={CURRENCY}") as r:
            if r.status == 200:
                js = await r.json()
                price = js[CONTRACT][CURRENCY]
                pricestring = (f"{NAME}: ${price}")
                return pricestring

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord! ')
    for guild in client.guilds:
        print("connected to ", guild.name)
    refresh_price.start()

@tasks.loop(seconds=float(REFRESH_TIMER))
async def refresh_price():
    for guild in client.guilds:
        await guild.me.edit(nick=await get_price())
client.run(TOKEN)
