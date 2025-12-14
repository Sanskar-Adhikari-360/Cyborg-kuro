import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/',intents=intents)

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

@bot.command()
async def updatebook(ctx,arg=None):
    if arg is None:
        await ctx.send("Please provide the name of the book to update.")
    else:
        await ctx.send(f"The currently reading book has been updated to: {arg}")

@bot.command()
async def updateshow(ctx,arg=None):
    if arg is None:
        await ctx.send("Please provide the name of the show to update.")
    else:
        await ctx.send(f"The currently watching show has been updated to: {arg}")

@bot.command()
async def updatemood(ctx,arg=None):
    if arg is None:
        await ctx.send("Please provide the mood you want to update to.")
    else:
        await ctx.send(f"Your cureent mood has been updated to {arg}.")


@bot.command()
async def update(ctx):
    await ctx.send("Which part of the website do you want to update??")
    embed = discord.Embed(title="Website Update Options", description="Choose an option below:")
    embed.add_field(name="1. Update the curently reading book", value=" Use /updatebook command",inline=False)
    embed.add_field(name="2. Update the curently watching show", value=" Use /updateshow command",inline=False)
    embed.add_field(name="3. Update the mood", value=" Use /updatemood command",inline=False)
    embed.add_field(name="4. Update the to do list", value=" Use /addtask command to add a new task \n" \
    "Use /removetask to remove a task \n " \
    "Use /checkoff on the completed task \n" \
    "Use /task to view all the tasks",inline=False)
    await ctx.send(embed=embed)



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