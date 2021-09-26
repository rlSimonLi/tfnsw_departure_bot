from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound
from env import Token
import os

TOKEN = None
client = None

if os.environ['BOT_MODE'] == 'production':
    TOKEN = Token.production_token
    client = commands.Bot(command_prefix='!')
elif os.environ['BOT_MODE'] == 'development':
    TOKEN = Token.development_token
    client = commands.Bot(command_prefix='?')
else:
    raise Exception("Please specify the bot mode.")

# remove the default help function
client.remove_command('help')

# load cogs specified
cogs = ('basic', 'dice', 'help', 'meme', 'mod', 'commute', 'role')
for cog in cogs:
    try:
        client.load_extension(f'cogs.{cog}')
    except ExtensionNotFound:
        print(f'cogs.{cog} is not found and is ignored.')
    else:
        print(f'cogs.{cog} is loaded.')

print("Student Centre is opening...")
client.run(TOKEN)
