import json,os,discord,threading,asyncio
from flask import Flask, redirect
from discord.ext import commands
from discord.commands import slash_command, Option
from config import tk, localurl, owner
from urllib.parse import urlparse


def web():
    app = Flask(__name__)
    
    @app.route("/<num>")
    def reurl(num):
        
        if os.path.isfile(f"reurl/{num}.json"):
            with open(f"reurl/{num}.json","r") as file:
                data = json.load(file)
                
            url = data["url"]
            with open(f"reurl/{num}.json","w") as file:
                data["time"] += 1
                json.dump(data,file)
            
            return redirect(url)
        
        else:
            
            return "您所要求連結無效"
    

    app.run(host="0.0.0.0",port="50006")

bot = commands.Bot(help_command=None,intents=discord.Intents.all())


@bot.event
async def on_ready():
    
    print("Reurl Is Runing")
    print("Make By yufuchen2011")
    
    
@bot.slash_command(description=f"生成一個{localurl}短網址")
async def create(ctx,re:Option(str,"短網址後綴"),url:Option(str,"要轉換的網址(記得加上https://)")):
    
    
    if ctx.author.id != int(owner):
        return await ctx.respond("您不是機器人擁有者無法使用\nYou Are Not The Owner For This Bot")
    if os.path.isfile(f"reurl/{re}.json"):
        return await ctx.respond("很抱歉!該連結無法使用,請換個連結\nSorry! This Link Can Not Use Please Change The Link")
    if url.startswith("https://") or url.startswith("http://"):
        pass
    else:
        return await ctx.respond("連結請加上 https:// 或者 http://\nPlease Add https:// or http:// To Your Link")
    
    try: #檢查是否有效
        result = urlparse(url)
        all([result.scheme, result.netloc])
    except:
        return await ctx.respond("這不是一個連結\nThis Is Not a Link")
    with open(f"reurl/{re}.json","w") as file:
        data = {"time":0,"url":url}
        json.dump(data,file)

    await ctx.respond(f"連結生成成功:{localurl}/{re}")
    
@bot.slash_command(description="清空所有短連結")
async def clean(ctx):
    if ctx.author.id != int(owner):
        return await ctx.respond("您不是機器人擁有者無法使用\nYou Are Not The Owner For This Bot")
    for filename in os.listdir("./reurl"):
        os.remove(filename)
    await ctx.respond("已成功清除所有短網址")
    
@bot.slash_command(description="管理短網址")
async def admin(ctx,url:Option(str,"要管理的網址後綴")):
    if ctx.author.id != int(owner):
        embed = discord.Embed(description="您不是機器人擁有者無法使用\nYou Are Not The Owner For This Bot", color=discord.Colour.red())
        return await ctx.respond("Error",embed=embed)
    if not os.path.isfile(f"reurl/{url}.json"):
        embed = discord.Embed(description="找不到該網址\nUrl Is Not Defined", color=discord.Colour.red())
        return await ctx.respond("Error",embed=embed)
    with open(f"reurl/{url}.json","r") as file:
        data = json.load(file)
        time = data["time"]
        reurl = data["url"]
        
    embed = discord.Embed(title=url,description=f"{localurl}/{url}網址管理中心", color=discord.Colour.random())
    embed.add_field(name="使用次數", value=f"已使用 {time} 次", inline=True)
    embed.add_field(name="網址導向", value=f"網址導向 {reurl}", inline=True)
    await ctx.respond("資料載入完成",embed=embed)

t = threading.Thread(target=web)
t.start()
bot.run(tk)