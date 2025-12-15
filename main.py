import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json
import subprocess
from datetime import datetime
import asyncio


data = {}

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix='/',intents=intents)

def git_push():
    subprocess.run(["git", "add", "data.json"], check=True)
    subprocess.run([
        "git", "commit",
        "-m", f"Update status ({datetime.now().isoformat()})"
    ], check=True)
    subprocess.run(["git", "push"], check=True)


@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "meow" in message.content.lower():
        await message.channel.send(f"{message.author.mention} - meow meow meow!! :smirk_cat: :smirk_cat: :smirk_cat: ")
    
    await bot.process_commands(message)
    
@bot.command()
async def greet(ctx):
    await ctx.send(f"Ni hao fine shyt :smirk_cat: :smirk_cat:  {ctx.author.mention}!")
    
@bot.command()
async def poll(ctx,*,question):
    embed =  discord.Embed(title="Polll time babby!!", description=question)
    poll_message =  await ctx.send(embed=embed)
    await poll_message.add_reaction("👍🏿")
    await poll_message.add_reaction("👎🏿")

@bot.command()
async def website(ctx):
    await ctx.send("Your website is https://marss.nekoweb.org :)"
                   " Do you need any assistance on it??")


async def update_task(ctx,subcommand,arg,message1, message2):
    if arg is None:
        await ctx.send(message1)
    else:
        data[subcommand] = arg
        print(f"Updating {subcommand} with value: {arg}")
        await ctx.send(f"{message2}: **{arg}**")
        
@bot.command()
async def update(ctx, subcommand, *, arg=None):
    global data
    match subcommand:
        case "book":
            return await update_task(ctx,subcommand,arg,"Please provide the name of the book to update.","The currently reading book has been updated to")
        case "show":
           return await update_task(ctx,subcommand,arg,"Please provide the name of the show to update.","The currently watching show has been updated to")
        case "mood":
            return await update_task(ctx,subcommand,arg,"Please provide the mood you want to update to.","Your cureent mood has been updated to")
        case _:
            await ctx.send("Invalid command:<")
        

@bot.command()
async def commit(ctx):
    await ctx.send("Do you want to commit the following changes to the GitHub repository?")
    embed = discord.Embed(title="Pending Changes", description="Here are the current changes to be committed:")
    global data
    for key, value in data.items():
        embed.add_field(name=key.capitalize(), value=value, inline=False)
    await ctx.send(embed=embed)
    await ctx.send("Use /y to confirm and push the changes to GitHub and /n to cancel the commit.")
    try:
        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send("No response received. Commit operation cancelled.")
        return
    if response.content.lower() == '/y':
        await ctx.send("Committing the changes in the JSON...")
        with open('data.json', 'w') as f:
            json.dump(data, f)
        await ctx.send("Changes have been committed successfully!")
        git_push()
        await ctx.send("Changes have been pushed to the GitHub repository successfully!")
    elif response.content.lower() == '/n':
        await ctx.send("Commit operation cancelled.")


@bot.command()
async def helpme(ctx):
    await ctx.send("Here are the available commands:\n")
    embed = discord.Embed(title="Help Menu", description="List of available commands")
    embed.add_field(name="/greet", value="Greets the user.", inline=False)
    embed.add_field(name="/poll <question>", value="Creates a poll with the given question.", inline=False)
    embed.add_field(name="/website", value="Provides the website link.", inline=False)
    embed.add_field(name="/helpme", value="Displays this help message.", inline=False)
    await ctx.send(embed=embed)
    
bot.run(token, log_handler=handler, log_level=logging.DEBUG)

