import discord
from discord.embeds import Embed
from discord.ext import commands
import feedparser
from datetime import date
from image_downloader import download

DISCORD_TOKEN = "Nzg1NTcwMDc5NTMzNDMyODky.X85xJg.n0YAfX14qhwpvG61gZi7Mkb_P0o"
DESC = "Bot for shitting and farting"

log_message = "{user} -- {command} -- {time}"

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
async def day(ctx):
	print(log_message.format(user=ctx.message.author,command="day",time=date.today()))
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
async def shaker(ctx):
	print(log_message.format(user=ctx.message.author,command="shaker",time=date.today()))
	await ctx.send(file=discord.File("images/bluebison.jpg"))
bot.run(DISCORD_TOKEN)