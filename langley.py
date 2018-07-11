import sys
import re
import random as rand
import json
import urllib.error
from urllib.request import urlopen
import discord
from discord.ext.commands import Bot

with open('tokens.txt') as f:
    tokens = f.read().splitlines()

with open('admins.txt') as f:
    admin_list = f.read().splitlines()
    
with open('vars.txt') as f:
    vars = f.read().splitlines()
    
'''
Tokens file line designations:
0: Discord api key
1: Backpack.tf api key

Vars file line designations:
0: SCP Series number 
'''

client = Bot(command_prefix = ">")

#helper functions
def cleanhtml(raw): #remove tags from an HTML dump
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw)
  return cleantext
  
def split_on(source, o_string, c_string): #give text between two parts of a string
    return str(source.split(o_string,1)[1].split(c_string,1)[0])

#put commands in alphabetical order

@client.command()
async def ask():
    def answer(argument):
        switcher = {
            1: "yes",
            2: "totally",
            3: "no",
            4: "nah",
            5: "maybe",
            6: "I'm not sure"
        }
        return switcher.get(argument, "I don't know")
    await client.say(answer(rand.randint(1,6)))
    
@client.command(pass_context = True)
async def e(ctx):
    if str(ctx.message.author) in admin_list:
        try:
            result = str(eval(str(ctx.message.content[3:])))
            await client.say('`' + result + '`')
        except Exception as e:
            await client.say('`' + 'Error: ' + str(e) + '`')
    else:
        await client.say("run your own programs, ya leech")

@client.command()
async def hello():
    await client.say("hello!")
    
@client.command(pass_context = True)
async def kill(ctx):
    if str(ctx.message.author) in admin_list:
        await client.say("goodbye cruel world! :joy: :gun:")
        await client.logout()
        exit()
    else:
        await client.say("you can't kill me you pathetic fleshling!")
    
@client.command()
async def random(low, high):
    try:
        answer = str(rand.randint(int(low), int(high)))
        await client.say(answer)
    except ValueError:
        await client.say("I need numbers, dingbat")
        
@client.command()
async def scp(num):
    if num == "random":
        num = str(rand.randint(1, int(vars[0]) * 1000))
        if int(num) < 10:
            num = "00" + num
        elif int(num) < 100:
            num = "0" + num
        
    url = "http://www.scp-wiki.net/scp-" + num
    
    try: 
        page = cleanhtml(str(urlopen(url).read()))
        
        try:
            itemno = split_on(page, "Item #:", "\\n")
        except IndexError:
            itemno = " ERROR"
        
        try:
            oclass = split_on(page, "Class:", "\\n")
        except IndexError:
            oclass = " ERROR"
       
        await client.say("**Item #:**" + itemno)
        await client.say("**Object Class:**" + oclass)
        await client.say("**Documentation: **" + url)
        urlopen(url).close()
    except urllib.error.HTTPError as e:
        code = e.code
        if code == 404:
            await client.say("SCP-" + num + " does not exist")    
        else:
            print(code)
            await client.say("Cannot display SCP-" + num)
          
@client.command(pass_context = True)
async def status(ctx):
    if str(ctx.message.author) in admin_list:
        await client.say("blah")
    else:
        await client.say("getting a bit nosey, are we?")

@client.command(pass_context = True)
async def tf2price(ctx, quality):
    quality = quality.title()
    qualities = {
        "Normal"           :0,
        "Genuine"          :1,
        "rarity2"          :2,
        "Vintage"          :3,
        "rarity3"          :4,
        "Unusual"          :5,
        "Unique"           :6,
        "Community"        :7,
        "Valve"            :8,
        "Self-Made"        :9,
        "Customized"       :10, 
        "Strange"          :11,
        "Completed"        :12, 
        "Haunted"          :13,
        "Collector's"      :14,
        "Decorated Weapon" :15
    }
    
    if quality not in qualities:
        qual = "Unique"
        cutoff = 10
    else:
        qual = str(qualities.get(quality, "Unique"))
        cutoff = 11 + len(quality)
    
    item = ctx.message.content[cutoff:]
   
    try:
        url = "https://backpack.tf/api/IGetPriceHistory/v1?format=json&item=" + item.title().replace(" ", "+") + "&quality=" + qual + "&key=" + str(tokens[1])
    
        page = urlopen(url).read()
        data = json.loads(page)
    
        prices = str(data["response"]["history"][-1]).replace("'", "")
    
        low  = split_on(prices, "value: ", ",")
        high = split_on(prices, "value_high: ", ",")
        currency = split_on(prices, "currency: ", ",")
    
        await client.say("**{0} - {1} {2}**".format(low, high, currency))
    except json.decoder.JSONDecodeError:
        await client.say("Unable to fetch item prices. Item may not exist or may not posess the item quality desired. Please ensure that the item's name and quality are correct.")

    
@client.command()
async def uwu():
    def emoticons(argument):
        switcher = {
            1: "(◠‿◠✿)",
            2: "(◕ᴗ◕✿)",
            3: "(ꈍ ꒳ ꈍ✿)",
            4: "(ʘ‿ʘ✿)",
            5: "（✿ ͡◕ ᴗ◕)つ━━✫・*。",
            6: "≧❀‿❀≦",
            7: "⊂(◉‿◉)つ",
            8: "(ΘεΘ;)",
            9: "( ͡~ ͜ʖ ͡°)",
            10: "(≧∇≦)",
            11: "Ｕ^皿^Ｕ",
            12: "(╯ಠ‿ಠ)╯︵┻━┻"
        }
        return switcher.get(argument, "Invalid UWU")
    await client.say(emoticons(rand.randint(1, 12)))

client.run(tokens[0])