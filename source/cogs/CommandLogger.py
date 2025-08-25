from discord.ext import commands
import datetime
import os
print("Current working directory:", os.getcwd())

# Make sure the logs folder exists
os.makedirs("logs", exist_ok=True)
LOG_FILE = "logs/command_log.txt"

def log_command_locally(entry: str):
    """Append a log entry to the local file with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {entry}\n")

class CommandLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        log_command_locally(f"{ctx.author} used '{ctx.command}' in #{ctx.channel}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            log_command_locally(f"{ctx.author} tried '{ctx.command}' without permission in #{ctx.channel}")
        elif isinstance(error, commands.MissingRequiredArgument):
            log_command_locally(f"{ctx.author} failed '{ctx.command}' (missing arguments) in #{ctx.channel}")
        else:
            log_command_locally(f"{ctx.author} encountered error in '{ctx.command}' in #{ctx.channel}: {error}")

async def setup(bot):
    await bot.add_cog(CommandLogger(bot))
