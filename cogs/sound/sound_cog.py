import discord
from discord.ext import commands

from datetime import datetime
import time
#It infuriates me that this module has to be imported; I can't find a way to handle lengths of audio files natively in discord.py, so this was the only implementation I could find that didn't involve manually checking the lengths of each audio file added.
from mutagen.mp3 import MP3

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

class SoundCog(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
		self.error=":x: *{error}* :x:"

	def log(self,func,member,error=False):
		if not error:
			print(f"{bcolors.OKGREEN}Success: {bcolors.ENDC}{bcolors.OKBLUE}SoundCog.{bcolors.ENDC}{bcolors.OKCYAN}{func}{bcolors.ENDC} called by {bcolors.HEADER}{member}{bcolors.ENDC} || {bcolors.BOLD}{datetime.now()}{bcolors.ENDC}")
		else:
			print(f"{bcolors.FAIL}Error:   {bcolors.ENDC}{bcolors.OKBLUE}SoundCog.{bcolors.ENDC}{bcolors.OKCYAN}{func}{bcolors.ENDC} called by {bcolors.HEADER}{member}{bcolors.ENDC} || {bcolors.BOLD}{datetime.now()}{bcolors.ENDC}")
	
	@commands.command(name="dc")
	async def dc(self,ctx):
		"""
		Doesn't really work; meant to forcibly dc the bot even when it is playing something, but I have to read the documentation more to actually work out how audio is handeled by discord.
		"""
		vc = ctx.voice_client
		await vc.disconnect()
		self.log("dc",ctx.message.author)

	async def play_sound(self,ctx,sound):
		"""
		This cog has a bit of an odd implementation; it was meant to be a soundboard, basically, where I can just ask an audio file and do minimal work to allow it to be used.
		To avoid re-writing the logic below for every sound, I made this function, then, as you'll see below, each following function just calls this function with the name of the audio file as a parameter

		I have a feeling there is a better way to do something better, by writing code that searches the utils/resources/sounds file and generates functions for them from their names, but that will be for another day...

		"""
		if not ctx.author.voice:
					await ctx.send(self.error.format(error="You are not in a VC"))
					self.log(sound,ctx.message.author,True)
		else:
			connection = ctx.bot.voice_clients
			if len(connection) == 0:
				channel = ctx.author.voice.channel
				await channel.connect()

			vc = ctx.voice_client
			if vc.is_playing():
				await ctx.send(self.error.format(error="Bot already playing sound, please try again after it is done"))
				self.log(sound,ctx.message.author,True)
			else:
				vc.play(discord.FFmpegPCMAudio(f'utils/resources/sounds/{sound}.mp3'),after=lambda e: True)
				time.sleep(MP3(f'utils/resources/sounds/{sound}.mp3').info.length)
				await vc.disconnect()
				self.log(sound,ctx.message.author)

	@commands.command(name="shutup")
	async def shutup(self,ctx):
		"""
		A classic
		"""
		await self.play_sound(ctx,"shutupbitch")

	@commands.command(name="ping")
	async def ping(self,ctx):
		"""
		To annoy
		"""
		await self.play_sound(ctx,"ping")

	@commands.command(name="holypanda")
	async def holypanda(self,ctx):
		"""
		For the keyboard-lovers
		"""
		await self.play_sound(ctx,"holypanda")


def setup(bot):
	bot.add_cog(SoundCog(bot))