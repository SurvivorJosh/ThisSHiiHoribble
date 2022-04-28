import requests
import os
import sys
import threading
import time
import json
import asyncio
import discord
import aiohttp
from colorama import Fore
import random
from discord import Webhook, AsyncWebhookAdapter
from pystyle import Colorate, Colors, Write
from discord.ext import commands

os.system(f'cls & mode 85,20 & title [Taifun] Token Login')

token = input(f'Token: ')


os.system('cls')

def check_token():
    if requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": f'{token}'}).status_code == 200:
        return "user"
    else:
        return "bot"




token_type = check_token()
intents = discord.Intents.all()
intents.members = True

if token_type == "user":
    headers = {'Authorization': f'{token}'}
    client = commands.Bot(command_prefix=">", case_insensitive=False, self_bot=True, intents=intents)
elif token_type == "bot":
    headers = {'Authorization': f'Bot {token}'}
    client = commands.Bot(command_prefix=">", case_insensitive=False, intents=intents)

client.remove_command("help")

class Taifun:

    def __init__(self):
        self.name = 'Taifun'
        
               
    def spam(self, message, webhookurl):

        try:
            r = requests.post(webhookurl, json={"content": message})
            s = [200, 201, 204]
            if r.status_code in s:
                print(Colorate.Horizontal(Colors.green_to_cyan, f"Sent Message > {message}"))
            elif r.status_code == 429:
                b = r.json()
                print(Colorate.Horizontal(Colors.yellow_to_red, f"Ratelimited, retrying in {b['retry_after']} seconds"))
                
        except:
            print(Colorate.Horizontal(Colors.yellow_to_red, "Bad Webhook > " + webhookurl))


    def BanMembers(self, guild, member):
        while True:
            r = requests.put(f"https://discord.com/api/v9/guilds/{guild}/bans/{member}", headers=headers)
            if 'retry_after' in r.text:
                b = r.json()
                print(Colorate.Horizontal(Colors.red_to_purple, f"RateLimited, retrying {b['retry_after']} seconds"))
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(Colorate.Horizontal(Colors.blue_to_purple, f"Banned {member.strip()}"))
                    break
                else:
                    break
    
    async def spamming(self):
        message = input(Colorate.Horizontal(Colors.red_to_purple, f'[>] Spam Message: '))
        webhookurl = input(Colorate.Horizontal(Colors.red_to_purple, f'[>] Webhook Url: '))
        amount = input(Colorate.Horizontal(Colors.red_to_purple, f'[>] Amount: '))

        for i in range(int(amount)):
            threading.Thread(target=self.spam, args=(message, webhookurl,)).start()

    async def Scrape(self):
        guild = input(Colorate.Horizontal(Colors.red_to_purple, f'[>] Guild Id: '))
        await client.wait_until_ready()
        guildOBJ = client.get_guild(int(guild))
        members = await guildOBJ.chunk()

        try:
            os.remove("Scraped/members.txt")
        except:
            pass

        membercount = 0
        with open('Scraped/members.txt', 'a') as m:
            for member in members:
                m.write(str(member.id) + "\n")
                membercount += 1
            print(Colorate.Horizontal(Colors.blue_to_green, f"Scraped Members: {membercount}"))
            m.close()
            

    async def BanAll(self):
        guild = input(Colorate.Horizontal(Colors.red_to_purple, f'[>] Guild Id: '))
        print()
        members = open('Scraped/members.txt')
        for member in members:
            threading.Thread(target=self.BanMembers, args=(guild, member,)).start()
        members.close()


    async def Menu(self):

        os.system(f'cls & mode 85,20 & title Connected as {client.user} [Taifun]')
        print(Colorate.Horizontal(Colors.blue_to_purple, f'''

           ::::::::::: :::     ::::::::::: :::::::::: :::    ::: ::::    ::: 
              :+:   :+: :+:       :+:     :+:        :+:    :+: :+:+:   :+:  
             +:+  +:+   +:+      +:+     +:+        +:+    +:+ :+:+:+  +:+   
            +#+ +#++:++#++:     +#+     :#::+::#   +#+    +:+ +#+ +:+ +#+    
           +#+ +#+     +#+     +#+     +#+        +#+    +#+ +#+  +#+#+#     
          #+# #+#     #+#     #+#     #+#        #+#    #+# #+#   #+#+#      
         ### ###     ### ########### ###         ########  ###    ####                                                      
        ''', 1))
        print(Colorate.Horizontal(Colors.red_to_purple, '''
                                            Made by: Lone#6456
             (1) MassBan
             (2) Scrape
             (3) Webhook Spam
             (x) Exit
        ''', 1))

        choice = input(Colorate.Horizontal(Colors.red_to_purple, f'[>] Choose: '))
        if choice == '1':
            await self.BanAll()
            time.sleep(2)
            await self.Menu()
        elif choice == '2':
            await self.Scrape()
            time.sleep(3)
            await self.Menu()
        elif choice == '3':
            await self.spamming()
            time.sleep(2)
            await self.Menu()
        elif choice == 'X' or choice == 'x':
            os._exit(0)

    @client.event
    async def on_ready():
        await Taifun().Menu()
            
    def Startup(self):
        try:
            if token_type == "user":
                client.run(token, bot=False)
            elif token_type == "bot":
                client.run(token)
        except:
            print(f'{self.colour}> \033[37mInvalid Token')
            input()
            os._exit(0)

if __name__ == "__main__":
    Taifun().Startup()