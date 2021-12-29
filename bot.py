#!/usr/bin/python3
import discord
from discord.ext import commands
from urllib import parse, request
import re
import os
import datetime
import requests

##################
###  COMANDOS  ###
##################

# Caracter por el cual identifica si se dirige al bot
bot = commands.Bot(command_prefix='$', description="Bot de auditoria web")

### 1- Muestra todos los comandos disponibles ###
@bot.command()
async def ayuda(ctx):
    await ctx.send("```php\n Esto es lo que buscas: \n $ayuda Muestra los comandos permitidos \n $info Informacion del servidor \n $ping Testeo de respuesta \n $sub Introduce una pagina y te muestra sus subdominios \n $take Indica si existe un subdominio vulnerable al SubdomainTakeOver \n $dir Codigo de respuesta del directorio indicado ej: $dir google.es /robots.txt \n $bitcoin Precio del bitcoin actual```")

### 2- Muestra infomacion sobre el discord ###
@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Informacion sobre el servidor", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    #embed.set_thumbnail(url="<url_icon>")
    await ctx.send(embed=embed)

### 3- Test de respuesta al poner $ping ###
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

### 4- Busca subdominios ###
@bot.command()
async def sub(ctx, domain):
    await ctx.send("Escaneando subdominios...")
    os.system("findomain -t" +  domain + "> /tmp/subs.txt")
    os.system("cat /tmp/subs.txt|egrep -v 'Searching'|egrep -v 'Job'|egrep -v 'Good' > /tmp/subdominios.txt")
    await ctx.send(file=discord.File(r'/tmp/subdominios.txt'))

### 5- Subdomain Takeover ###
@bot.command()
async def take(ctx, take):
    await ctx.send("Escaneando SubdomainTakeOvers...")
    os.system("findomain -t" +  take + "> /tmp/subdominios.txt")
    os.system("subzy --targets /tmp/subdominios.txt" + "> /tmp/subtakeover.txt")
    await ctx.send(file=discord.File(r'/tmp/subtakeover.txt'))

### 6- Rutas existentes ###
@bot.command()
async def dir(ctx, domain, rute):
    await ctx.send("Escaneando directorios...")
    os.system("findomain -t" +  domain + "> /tmp/subdominios.txt && subcheck /tmp/subdominios.txt " + rute + "> /tmp/dir.txt")
    os.system("cat /tmp/dir.txt|egrep -v '000'|egrep -v 'Searching'|egrep -v 'Job'|egrep -v 'Good' > /tmp/directorios.txt")
    await ctx.send(file=discord.File(r'/tmp/directorios.txt'))


### 7- Comando PELIGROSO!!! ###
#@bot.command()
#async def cmd(ctx, command):
#    os.system(command + "> /tmp/commands.txt")
#    f = open("/tmp/commands.txt",'r',encoding = 'utf-8')
#    await ctx.send(f.read())


### 8- Muestra el precio del bitcoin ###
@bot.command()
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await ctx.send("```json\n Bitcoin price is: " + value + " USD```")

################################
### Inicio de sesion del bot ###
################################
client = discord.Client()
# Que esta haciendo el bot
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await bot.change_presence(activity=discord.Game(name="Auditando Webs"))

bot.run('<BOT_TOKEN>')
