import discord
import re
import urllib.request
import subprocess
import time
import requests
import random
from discord.utils import get
import discord.utils
from datetime import datetime
from discord import Webhook, RequestsWebhookAdapter, File
import asyncio

client = discord.Client(heartbeat_timeout=600)

new_startup = True

async def log_message(log_entry):
    current_time_obj = datetime.now()
    current_time_string = current_time_obj.strftime("%b %d, %Y-%H:%M:%S.%f")
    print(current_time_string + " - " + log_entry, flush = True)

async def reply_message(message, response):
    if not message.guild:
        channel_name = dm_tracker[message.author.id]["commandchannel"].name
        server_name = str(dm_tracker[message.author.id]["server_id"])
    else:
        channel_name = message.channel.name
        server_name = message.guild.name
        
    await log_message("Message sent back to server " + server_name + " channel " + channel_name + " in response to user " + message.author.name + "\n\n" + response)
    
    message_chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
    for chunk in message_chunks:
        await message.channel.send(">>> " + chunk)
        asyncio.sleep(1)
        
@client.event
async def on_ready():
    await log_message("Logged in!")
@client.event
async def on_guild_join(guild):
    await log_message("Joined guild " + guild.name)
@client.event
async def on_guild_remove(guild):
    await log_message("Left guild " + guild.name)
    
@client.event
async def on_message(message):

   if message.content.startswith('/r'):


        command_string = message.content.split(' ')
        command = message.content.replace('/r ','')
        parsed_string = message.content.replace("/r " + command,"")
        parsed_string = re.sub(r"^ ","",parsed_string)
        username = message.author.name
        server_name = message.guild.name
        if re.search(command, parsed_string):
            parsed_string = ""
        await log_message("Command " + message.content + " called by " + username + " from " + server_name)
        
        if command == 'help' or command == 'info':
            response = "**D&D Bot**\n\n`/r xdy`: Roll x number of y dice.\n`/r invite`: Show a bot invite link.\n"
            await reply_message(message, response)
        elif command == 'invite':
            response = 'Click here to invite D&D bot: https://discord.com/api/oauth2/authorize?client_id=739310845871390791&permissions=67584&scope=bot'
            await reply_message(message, response)
        
        if re.search(r"\d+d\d+",message.content):
            if re.search(r"\s+",message.content):
                dice_string = message.content.replace('/r ','').split(' ')
            else:
                dice_string = [message.content.replace('/r ',''),]
            response = "**Dice roll:** "
            total_sum = 0
            next_operator = ''
            for operator in dice_string:
                sum = 0 
                print(str(operator))
                print(str(next_operator))
                if re.search(r"\d+d\d+",operator):
                    
                    dice_re = re.compile(r"(\d+)d(\d+)")
                    m = dice_re.search(operator)
                    if not m:
                        await reply_message(message, "Invalid dice command!")
                        return
                    number_of_dice = m.group(1)
                    dice_sides = m.group(2)
                    if int(number_of_dice) > 100:
                        await reply_message(message, "You can't specify more than 100 dice to roll!")
                        return

                    response = response + " ( "
                    for x in range(0, int(number_of_dice)):
                        die_roll = random.randint(1, int(dice_sides))
                        sum = sum + die_roll
                        response = response + " `" + str(die_roll) + "` + "
                    response = response.strip(' + ')  + " ) "

                elif operator == '+':
                    next_operator = '+'
                    response = response + " " + operator
                    continue
                elif operator == '-':
                    next_operator = '-'
                    response = response + " " + operator
                    continue
                elif operator == '*':
                    next_operator = '*'
                    response = response + " " + operator
                    continue
                elif operator == '/':
                    response = response + " " + operator
                    next_operator = '/'
                    continue
                elif re.search(r"[0-9]", operator):
                    m = re.search(r"([0-9]+)",operator)
                    if m:
                        sum = int(m.group(1))
                        response = response + " " + str(sum) + " "
                if next_operator == '+':
                    total_sum = total_sum + sum
                    
                elif next_operator == '-':
                    total_sum = total_sum - sum
                    
                elif next_operator == '*':
                    total_sum = total_sum * sum
                    
                elif next_operator == '/':
                    total_sum = total_sum / sum
                    
                if total_sum == 0:
                    total_sum = sum
                    
                
                print("Total sum: " + str(total_sum))
                
            response = response.replace(dice_string[0],'') + " = `" + str(total_sum) + "`"        
                    
            await reply_message(message, response)            
        else:
            pass
            
            
client.run('REDACTED')