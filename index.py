import discord
from discord.ext import commands

from datetime import datetime
import json

#from gtts import gTTS
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

with open("secrets.json","r") as f:
	secrets = json.load(f)

DISCORD_TOKEN = secrets["DiscordToken"]
DESC = "A pretty random bot, with random features shoved in when I feel like it"
f.close()

bot = commands.Bot(command_prefix = "*", description=DESC)
"""
Most of the code below is largely based on this example:
https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
"""
extensions = [
	"cogs.school.school_cog",
	"cogs.utility.utility_cog",
	"cogs.sound.sound_cog"
]

if __name__=="__main__":
	for extension in extensions:
		bot.load_extension(extension)

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name="My Life Fall Apart"))
	print(f"Logged in as: {bot.user.name}, running on Discord version {discord.__version__}")


@bot.event
async def on_command_error(ctx,error):
	"""
	Largely for development purposes.
	I was tired of having to scroll through my terminal to view errors, 
	as it really cluttered it, so this function saves it to an external 
	txt file and simpy prints that an error occured.
	"""
	with open("logs.txt","a") as f:
		f.write(f"\n{ctx}: {error}")
	f.close()
	
bot.run(DISCORD_TOKEN, bot=True, reconnect=True)