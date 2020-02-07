import discord
import os
import sys
import time 
import datetime
import pytz
import subprocess
from keep_alive import keep_alive
import math
import string
import asyncio
# import pythonping
# import csv
# from discord.ext import commands
# TODO: Add ping function 

print(sys.version)

client = discord.Client()

# Timezone Dictionary 
timezones_dictionary = {
  'asia/beijing': 'Asia/Shanghai',
  'roc': ''
}

guilds_csv = open('guilds.csv', 'a+')

# Get time
async def get_time(message, *args):

  if args:
    timezone_input = args[0]
  
  else:
    timezone_input = 'Australia/Sydney'

  try:
    timezone_input = timezones_dictionary[timezone_input.lower()]
  
  # Nothing to replace
  except KeyError:
    pass
  
  try:
    output_time = datetime.datetime.now(pytz.timezone(timezone_input))

  # Incorrect Timezone 
  except pytz.exceptions.UnknownTimeZoneError:
    return ('Unknown Timezone')
  
  # Output
  return output_time.strftime("%A %Y %B %d %H:%M:%S %Z %z")
  
async def ping(message, *args):
  if args:
    website = args[0]
    return ' '.join([i.decode("utf-8") for i in subprocess.check_output(["ping", website, "-c", "5"]).split()[-4:-1]])
  else:
    return str('The ping is ' + str(int(client.latency*1000))+ 'ms')
  
async def invite(message, *args):
  return 'https://discordapp.com/api/oauth2/authorize?client_id=596544931359883274&permissions=8&scope=bot'

async def get_help(message, *args):
  
  if args:
    if args[0] == 'time':
      return '''
        Time:
        time [timezone]: get time 
        common timezones:
        <https://pastebin.com/x2r9qX04>
      '''
    elif args[0] == 'calc':
      return '''
        Calc:
        calc <argument>: calculate
        Functions: 
        acos, acosh, asin, asinh, atan, atan2, atanh, ceil, copysign, cos, cosh, degrees, e, erf, erfc, exp, expm1, fabs, factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, inf, isclose, isfinite, isinf, isnan, ldexp, lgamma, log, log10, log1p, log2, modf, nan, pi, pow, radians, remainder, sin, sinh, sqrt, tan, tanh, tau, trunc
      
      '''
    else:
      return 'No additional information found'
  
  else:
    return '''
      Help:
      help [verb]: get help 
      calc <argument>: do calculations
      time [timezone]: get time
      ping [website]: ping website
      invite: invite bot
    '''      

async def calc(message, *args):
  if args:
    calculation = ' '.join(args)

    test_calculation = calculation
    for i in dir(math):
      test_calculation = test_calculation.replace(i, '0')

    for i in string.ascii_lowercase:
      if i in test_calculation.lower():
        return 'Unknown Operator'
    
    for i in dir(math):
      calculation = calculation.replace(i, 'math.'+i)

    return str(eval(calculation))
  else:
    return 'Argument required'

async def echo_a(message, *args):
  if any(
      [
        message.author.id in admins,
        message.author.id in mods,
      ]
    ):
    if args:
      return ' '.join(args)
    else:
      return 'Argument required'
  else:
    return 'Authorisation Failed'

async def echo(message, *args):
  if args:
    return str(
      '`'+
      str(message.author.name)+
      '#'+
      str(message.author.discriminator)+
      ':` '+
      ' '.join(args)
    )
  else:
    return 'Argument required'

async def kick(message, *args):

  if any(
      [
        message.author.id in admins,
        message.author.permissions_in(
          message.channel
        ).administrator,
      ]
    ):

    try:
      if args:
        await message.guild.kick(
          client.get_user(
            int(args[0])
          )
        )
        return 'Kicked'

      else:
        return 'Argument required'
    
    except discord.errors.Forbidden:
      return 'Error occured. Most likely error: Cannot kick admins'

async def debug(message, *args):
  if any(
      [
        message.author.id in admins,
      ]
    ):

    exec(' '.join(args))
  
    return 'Done'

async def log(message):

  # Log - log_channel
  # Try sepcific channel
  try:
    log_channel = client.get_channel(
      channels[message.channel.id]
    )

  except KeyError:  # Not specified channel
    pass
    
  # Try sepcific server
  try:
    log_channel = client.get_channel(
      channels[message.guild.id]
    )

  except KeyError:  # Channel not specified
    log_channel = client.get_channel(645903470079246349)
  except AttributeError:  # DMs
    log_channel = client.get_channel(649737935293251636)

  try:
    await log_channel.send(
      str(
        '```'+
          'Guild:      '+str(message.guild.name)+
        '\nGuild ID:   '+str(message.guild.id)+
        '\nChannel:    '+str(message.channel.name)+
        '\nChannel ID: '+str(message.channel.id)+
        '\nAuthor:     '+str(message.author.name)+
        '#'+str(message.author.discriminator)+
        '\nAuthor ID:  '+str(message.author.id)+
        '\nMessage:    '+str(message.content)
          .replace('```', '` ` `')+
        '\nMessage ID: '+str(message.id)+
        '```'
      )
    )
  except AttributeError:  # DMs
    await log_channel.send(
      str(
        '```'+
        '\nAuthor:     '+str(message.author.name)+
        '#'+str(message.author.discriminator)+
        '\nAuthor ID:  '+str(message.author.id)+
        '\nMessage:    '+str(message.content)
          .replace('```', '` ` `')+
        '\nMessage ID: '+str(message.id)+
        '```'
      )
    )

verbs = {
  'ping'  : ping,
  'time'  : get_time,
  'help'  : get_help,
  'invite': invite,
  'calc'  : calc,
  'echo'  : echo,
  'echoa' : echo_a,
  'kick'  : kick,
  'debug' : debug,
}

channels = {
  # Message channel : Log channel
  669120700124102678: 674814944394477599,  # Roo Nation W
  # Message guild   : Log channel 
  391120387326345217: 646999356821602304,  # Roo Nation 
  515761331798802434: 649191022563295254,  # Anarchy 
  520432120842289172: 649728449321238558,  # BTS
}

mods = []

admins = [
  349495401335750658, # Me
]


@client.event
async def on_ready():

  # Open guilds.txt
  guilds_file = open('guilds.txt', 'w')

  # Write guilds into guilds.txt
  for guild in client.guilds:
    guilds_file.write(str(guild.name+'\n'))

  # Close guilds file
  guilds_file.close()

  # Print ready
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  all_verbs = {**verbs}

  # Ignore self
  if message.author == client.user:
    return

  # Log message
  await log(message) 

  # If the bot is addressed
  if message.content.startswith('<@596544931359883274>') or message.content.startswith('<@!596544931359883274>'):

    async with message.channel.typing():

      # If a command exists
      if len(message.content.split()) >= 2:
        verb = message.content.split()[1]
        noun = message.content.split()[2:]
      
        try:
          # Execute verb
          output = await all_verbs[verb](message, *noun)
        except KeyError:
          output = 'Unknown Command'
        
        time.sleep(0.5)

        try:
          await message.channel.send(output)
        except discord.errors.HTTPException:
          await message.channel.send(
            'HTTP Exception. Likely errors include Message too long (>2000 characters) or Message too short (<1 characters)'
          )


keep_alive()  # Keep the bot alive
token = os.environ.get("BOT_TOKEN")  # Classified
client.run(token) # Start bot