import io
from datetime import datetime

import aiohttp
import telethon
import requests
from telethon import events
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

from tg_companion.tgclient import client



DOLAR_HELP = """
    **Test your internet speed using http://speedtest.net/**
"""

EURO_HELP = """
    **Test your internet speed using http://speedtest.net/**
"""

@client.CommandHandler(outgoing=True, command="dolar", help=DOLAR_HELP)
async def dolar(event):
    pasteURL = "http://tr.investing.com/currencies/usd-try"
    data = urlopen(Request(pasteURL, headers={'User-Agent': 'Mozilla'})).read()
    parse = BeautifulSoup(data)
    for dolar in parse.find_all('span', id="last_last"):
        liste = list(dolar)
        client.update_message(event, f"Dolar: {str(liste)}")



@client.CommandHandler(outgoing=True, command="euro", help=EURO_HELP)
async def dolar(event):
    pasteURL = "http://tr.investing.com/currencies/eur-try"
    data = urlopen(Request(pasteURL, headers={'User-Agent': 'Mozilla'})).read()
    parse = BeautifulSoup(data)
    for dolar in parse.find_all('span', id="last_last"):
        liste = list(dolar)
        client.update_message(event, f"Euro: {str(liste)}")