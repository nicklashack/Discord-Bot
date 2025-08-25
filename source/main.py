import discord
from discord.ext import commands
import os
import asyncio
from config import TOKEN, PREFIX

intents = discord.Intents.default()
intents.members = True # required to give out roles
intents.message_content = True # required for reading messages
intents.reactions = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


# Minimal test listener to check reactions
@bot.event
async def on_raw_reaction_add(payload):
    print("Reaction detected!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# loads in cogs with a try/except function to catch errors
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename not in ('__init__.py'):
            cog_name = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(cog_name)
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")

async def main():
    await load_cogs() #await loading cogs
    await bot.start(TOKEN) #starts the bot after cogs are loaded

asyncio.run(main())