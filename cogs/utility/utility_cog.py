import discord
from discord.ext import commands
from discord.embeds import Embed

from datetime import date,datetime
import time

import pytz
from pytz import timezone
import requests
import json

#Very repetitive to include this in every cog: maybe find a way to make this available to all cogs by overwriting commands.Cog class?
#Same with self.error and self.log()
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

class UtilityCog(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
		self.error = ":x: *{error}* :x:"

	def log(self,func,member,error=False):
		if not error:
			print(f"{bcolors.OKGREEN}Success: {bcolors.ENDC}{bcolors.OKBLUE}UtilityCog.{bcolors.ENDC}{bcolors.OKCYAN}{func}{bcolors.ENDC} called by {bcolors.HEADER}{member}{bcolors.ENDC} || {bcolors.BOLD}{datetime.now()}{bcolors.ENDC}")

		else:
			print(f"{bcolors.FAIL}Error:   {bcolors.ENDC}{bcolors.OKBLUE}UtilityCog.{bcolors.ENDC}{bcolors.OKCYAN}{func}{bcolors.ENDC} called by {bcolors.HEADER}{member}{bcolors.ENDC} || {bcolors.BOLD}{datetime.now()}{bcolors.ENDC}")

	@commands.command(name="covid")
	async def covid(self,ctx):
		"""
		Gets US covid data from the current day, from https://covidtracking.com
		"""
		r=requests.get("https://api.covidtracking.com/v1/us/daily.json")
		
		if r.status_code:
			text = json.loads(r.text)[0]
			totalPos = text['positive']
			totalHosp = text["hospitalizedCurrently"]
			totalDeaths = text["death"]
			incDeaths = text['deathIncrease']
			incHosp = text["hospitalizedIncrease"]
			incPos = text["positiveIncrease"]
			embed = Embed(
				title = "COVID Update",
				url="https://covidtracking.com/data/api",
				)
			embed.add_field(name="New Cases",value=incPos,inline=True)
			embed.add_field(name="New Hospitilizations",value=incHosp,inline=True)
			embed.add_field(name="New Deaths",value=incDeaths,inline=True)
			embed.add_field(name="Total Cases",value=totalPos,inline=True)
			embed.add_field(name="Total Hospitilizations",value=totalHosp,inline=True)
			embed.add_field(name="Total Deaths",value=totalDeaths,inline=True)

			await ctx.send(embed=embed)
			self.log("covid",ctx.message.author)

		else:
			await ctx.send(self.error.format("The API failed to respond!"))
			self.log("covid",ctx.message.author,True)

	@commands.command(name="shorten")
	async def shorten(self,ctx,url):
		"""
		Uses the api, https://api.shrtco.de, to shorten a given URL
		This function is rather slow, which may be due to the api being hosted in DE. Still, works well enough
		"""
		error_codes = ["No URL specified","Invalid URL","Rate limit reached, please wait to try again","IP address blocked","shrtcode already in use","Unknown error","No code","Invalid code","Missing params","Trying to shorten disallowed link"]
		r=requests.get(f"https://api.shrtco.de/v2/shorten?url={url}")
		text = json.loads(r.text)
		ok = text['ok']
		if ok:
			self.log("shorten",ctx.message.author)
			short_link = text['result']['full_short_link']	

			await ctx.send(f":scissors: __{short_link}__")
		else:
			self.log("shorten",ctx.message.author,True)
			status_code = text['status_code']
			await ctx.send(self.error.format(error_codes[status_code+1]))

	@commands.command(name='qr')
	async def qr(self,ctx,*data):
		"""
		This function use the https://image-charts.com QR code option. More graph options could be added, but a QR code generator seems the most useful.
		This function also has essentially no error handling built in yet; potential errors that could/have occured:
			[] no data given results in no qr code (easy to fix)
			[] too much data given?
			[] invalid data given?
		"""
		formatted_data = ""
		for i in data:
			formatted_data+="%20"
			formatted_data+=i
		url = f"https://image-charts.com/chart?chs=200x200&cht=qr&chl={formatted_data}&choe=UTF-8"
		r=requests.get(url)
		with open("utils/resources/images/qr_code.png","wb") as f:
			f.write(r.content)
		f.close()
		await ctx.send(file=discord.File("utils/resources/images/qr_code.png"))
		self.log("qr",ctx.message.author)

	@commands.command(name="github")
	async def github(self,ctx,person,repo):
		"""
		Super quick, super rough function that takes advantage of the github api to get how long ago a commit was made to a particular repo.
		This has, again, virtually no error handling as of yet
		This is also an INCREDIBLY dirty implementation; the github api gives dates in GMT, and as a string that had to be modified to be turned into a datetime object.
		"""
		r = json.loads(requests.get("https://api.github.com/repos/ottomated/CrewLink/commits/master").text)

		last_pushed=r["commit"]["author"]["date"]
		last_pushed_general = last_pushed[:10]
		last_pushed_time = last_pushed[11:-1]
		last_pushed_date = datetime(int(last_pushed_general[0:4]),int(last_pushed_general[5:7]),int(last_pushed_general[8:]),int(last_pushed_time[:2]),int(last_pushed_time[3:5]),int(last_pushed_time[6:]))
		last_pushed_date_pytz = last_pushed_date.replace(tzinfo=timezone("GMT"))
		now=datetime.now(pytz.timezone("GMT"))

		self.log("git",ctx.message.author)
		await ctx.send(f"Last Updated: *{now-last_pushed_date_pytz}*")

	@commands.command(name="v")
	async def v(self,ctx):
		"""
		Makes use of discord.py's built-in function to get the discord version. Not particullarly useful, but, well, its there
		"""
		await ctx.send(f"Discord version *{discord.__version__}*")


def setup(bot):
	bot.add_cog(UtilityCog(bot))