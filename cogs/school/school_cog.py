import discord
from discord.ext import commands
from discord.embeds import Embed
import os.path
from datetime import date,datetime
import feedparser
import json
from utils.image_downloader import download
from utils.calendar_api.g_calendar import get_current_day

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


class SchoolCog(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
		self.error = ":x: *{error}* :x:"

	def log(self,func,member,error=False):
		if not error:
			print(f"{bcolors.OKGREEN}Success: {bcolors.ENDC}{bcolors.OKBLUE}SchoolCog.{bcolors.ENDC}{bcolors.OKCYAN}{func}{bcolors.ENDC} called by {bcolors.HEADER}{member}{bcolors.ENDC} || {bcolors.BOLD}{datetime.now()}{bcolors.ENDC}")
		else:
			print(f"{bcolors.FAIL}Error:   {bcolors.ENDC}{bcolors.OKBLUE}SchoolCog.{bcolors.ENDC}{bcolors.OKCYAN}{func}{bcolors.ENDC} called by {bcolors.HEADER}{member}{bcolors.ENDC} || {bcolors.BOLD}{datetime.now()}{bcolors.ENDC}")

	@commands.command(name="today")
	async def today(self, ctx):
		"""
		Just gets the day, og function to test cog implementation
		"""
		self.log("today",ctx.message.author)
		await ctx.send(f":calendar: Today is: *{date.today()}*")

	@commands.command(name="schedule",aliases=['sched'])
	async def schedule(self, ctx, month="December"): 
		"""
		This function checks for an image in the utils/resources/images/schedules folder, and sends it if found. 
		This was, naturally, originally intended to be used for schedules, but could easily be changed to get any types of images...
		"""
		try:
			await ctx.send(file=discord.File(f"utils/resources/images/schedules/{month}.png"))
			self.log("schedule",ctx.message.author)
		except:
			await ctx.send(self.error.format(error="Schedule not found!"))
			self.log("schedule",ctx.message.author,error=True)

	@commands.command(name="upload_schedule")
	async def upload_schedule(self,ctx,month,url):
		"""
		Sister function to self.schedule.
		In my implementation, people who can use this function are limited; change values in secret.json to change this.
		"""
		with open("secrets.json","r") as f:
			data = json.load(f)
		
		allowed = data["BotPerms"]["Schedule"][0]
		f.close()
		if str(ctx.message.author)== allowed:

			if(download(url,month)):
				await ctx.send("Uploaded  :100:")
				self.log("upload_schedule",ctx.message.author,error=False)
			
			else:
				await ctx.send(self.error.format("The image failed to upload!"))
				self.log("upload_schedule",ctx.message.author,error=True)
		
		else:
			await ctx.send(self.error.format("You don't have permission to do that!"))
			self.log("upload_schedule",ctx.message.author,error=True)

	@commands.command(name="updates",aliases=["update"])
	async def updates(self,ctx,num=1):
		"""
		Gets data from an rss feed; the specific use of mine has been hiden in my secrets.json for my own privacy.
		Still, this basic structure shows how to use the feedparser library in python, as well as some basic discord embeds.
		"""
		with open("secrets.json","r") as f:
			data = json.loads(f)
		rssUrl = data["rssUrl"]
		NewsFeed = feedparser.parse(rssUrl)

		
		for i in range(int(num)):
			title = NewsFeed.entries[i]['title']
			published = NewsFeed.entries[i].published
			link = NewsFeed.entries[i]['links'][0]['href']

			embed = Embed(
				title=title,
				url=link,
				description=f"Published: *{published}*"
				)
			await ctx.send(embed=embed)

		self.log("updates",ctx.message.author)

	@commands.command(name="day")
	async def day(self,ctx):
		"""
		Uses the Google Calendar API (in utils/calendar_api) to access my personal email, checking for a particular event today. A lot of this has been censored for privacy.
		"""
		current_day = get_current_day()
		if current_day:
			await ctx.send(f":blue_circle: **{current_day}** :blue_circle:")
			self.log("day",ctx.message.author)
		else:
			self.log("day",ctx.message.author,True)

def setup(bot):
	bot.add_cog(SchoolCog(bot))