import discord
from discord.embeds import Embed
from discord.ext import commands
import feedparser
from datetime import date
from image_downloader import download
import requests
import json
from calendar_api import get_current_day,get_upcoming_events

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

DISCORD_TOKEN = "Nzg1NTcwMDc5NTMzNDMyODky.X85xJg.n0YAfX14qhwpvG61gZi7Mkb_P0o"
DESC = "Bot for shitting and farting"

log_message = "   \033[94m{user}\033[0m   ---   \033[92m{command}\033[0m   @   \033[93m{time}\033[0m"

bot = commands.Bot(command_prefix = "*", description=DESC)

@bot.event
async def on_ready():
	print(f"Logged in as: {bot.user.name}")

@bot.command()
async def schedule(ctx,month="December"): 
	print(log_message.format(user=ctx.message.author,command="schedule",time=date.today()))
	try:
		await ctx.send(file=discord.File(f"images/schedules/{month}.png"))
	except:
		await ctx.send("Error! Make sure you spelled the month right")

@bot.command()
async def upload_schedule(ctx,month,url):
	print(log_message.format(user=ctx.message.author,command="upload_schedule",time=date.today()))
	if str(ctx.message.author)== "LOUIS#3375" or str(ctx.message.author)=="arrow#7963":
		schedules[month] = url
		download(url,month)
		await ctx.send("Uploaded")
	else:
		await ctx.send("You don't have permission to do that you little shit")

@bot.command()
async def today(ctx):
	print(log_message.format(user=ctx.message.author,command="today",time=date.today()))
	asdf = date.today()
	await ctx.send(f"The day is {asdf}")

@bot.command()
async def updates(ctx, num=1):
	print(log_message.format(user=ctx.message.author,command="updates",time=date.today()))
	NewsFeed = feedparser.parse("https://www.northcolonie.org/feed")
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

@bot.command()
async def covid(ctx, time="daily"):
	print(log_message.format(user=ctx.message.author,command="covid",time=date.today()))
	r=requests.get("https://api.covidtracking.com/v1/us/daily.json")
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

@bot.command()
async def day(ctx):

	print(log_message.format(user=ctx.message.author,command="day",time=date.today()))
	await ctx.send(get_current_day())

@bot.command()
async def calendar(ctx,options):
	print(log_message.format(user=ctx.message.author,command="calendar",time=date.today()))
	"""
	res = get_upcoming_events(int(options))
	embed = Embed(
		title=f"{options} Upcoming Events",
		url="https://calendar.google.com/calendar/u/2/r?cid=brk702seqlsta8a1ac8vet4bvk@group.calendar.google.com&cid=rqloirqi6lt10phpeggld0b3g0@group.calendar.google.com&cid=b2pa2hr349brm17qbjqk5t05ls@group.calendar.google.com&cid=g8nmr41ik3ijul1p4nvqubaq6g@group.calendar.google.com&cid=9tfs342l2p8q2sufh4sisjb3lk@group.calendar.google.com&cid=klsh48rf6vd3lqsfrvafdvr6b0@group.calendar.google.com&cid=9i14aufrnvmsalodjls87b1rrs@group.calendar.google.com&cid=ufoj7ecp2tko1l2hqcmu9rm3n8@group.calendar.google.com&cid=8s7g5c61v1jqaklpgg2i1lu9do@group.calendar.google.com&cid=en.usa%23holiday@group.v.calendar.google.com&cid=nccsk12.org_4tbpei4v6odq3kpt1jljv5cr8c@group.calendar.google.com&pli=1"
		)
	for i in res:
		embed.add_field(name=i[0],value=i[1],inline=True)

	await ctx.send(embed=embed)
"""
	get_upcoming_events(int(options))
	await ctx.send("placehollder")
@bot.command()
async def shaker(ctx):
	print(log_message.format(user=ctx.message.author,command="shaker",time=date.today()))
	await ctx.send(file=discord.File("images/bluebison.jpg"))
	
bot.run(DISCORD_TOKEN)