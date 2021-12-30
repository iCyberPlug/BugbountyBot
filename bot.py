#!/usr/bin/python3
import discord
from discord.ext import commands
from urllib import parse, request
import os
import datetime
import requests

##################
###  COMMANDS  ###
##################

# Character by which it identifies if it goes to the bot
# Description bot
bot = commands.Bot(command_prefix='$', description="Web audit bot")

### 1- Show all available commands ###
@bot.command()
async def ayuda(ctx):
    await ctx.send("```bash\n Results: \n $show Show allowed commands. \n $info Server information. \n $sub Enter a page and show you its subdomains. Example: $sub discord.com \n $take Indicates whether there is a subdomain vulnerable to SubdomainTakeOver. Example: $take discord.com \n $dir Status code of the indicated directory of all subdomains. Example: $dir discord.com /robots.txt \n $bitcoin Current bitcoin price.```")

### 2- Displays information about the discord ###
@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Information about the server", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    #embed.set_thumbnail(url="<url_icon>")
    await ctx.send(embed=embed)

### 3- Looking for subdomains ###
@bot.command()
async def sub(ctx, domain):
    await ctx.send("Scanning subdomains...")
    os.system("findomain -t" +  domain + "> /tmp/subs.txt")
    os.system("cat /tmp/subs.txt|egrep -v 'Searching'|egrep -v 'Job'|egrep -v 'Good'|egrep -v 'Target ==>' > /tmp/subdomains.txt")
    await ctx.send(file=discord.File(r'/tmp/subdomains.txt'))

### 4- Subdomain Takeover ###
@bot.command()
async def take(ctx, take):
    await ctx.send("Looking for SubdomainTakeOver...")
    os.system("findomain -t" +  take + "> /tmp/subs.txt")
    os.system("cat /tmp/subs.txt|egrep -v 'Searching'|egrep -v 'Job'|egrep -v 'Good'|egrep -v 'Target ==>'|httprobe --prefer-https > /tmp/subdomains.txt")
    os.system("subzy --targets /tmp/subdomains.txt" + "> /tmp/take.txt")
    os.system("cat /tmp/take.txt|egrep -v 'Loaded'|egrep -v 'default'|egrep -v 'Concurrent'|egrep -v 'verify_ssl'|egrep -v 'timeout'|egrep -v 'hide_fails'|sed 's|[]\[]0m| |g'|sed 's|[]\[]31m| |g' > /tmp/subtakeover.txt")
    await ctx.send(file=discord.File(r'/tmp/subtakeover.txt'))

### 5- See Directories Status ###
@bot.command()
async def dir(ctx, domain, rute):
    await ctx.send("Scanning directories...")
    os.system("findomain -t" +  domain + "> /tmp/subs.txt")
    os.system("cat /tmp/subs.txt|egrep -v 'Searching'|egrep -v 'Job'|egrep -v 'Good'|egrep -v 'Target ==>'|httprobe --prefer-https > /tmp/subdominains.txt")
    os.system("subcheck /tmp/subdomains.txt " + rute + "> /tmp/directories.txt")
    await ctx.send(file=discord.File(r'/tmp/directories.txt'))

### 6- Shows the price of bitcoin ###
@bot.command()
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await ctx.send("```json\n Bitcoin price is: " + value + " USD```")

#################
### Bot Login ###
#################
# Bot activities
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="Auditing Websites"))

bot.run('<BOT_TOKEN>')
