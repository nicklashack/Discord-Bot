from discord.ext import commands
import discord
import datetime
import os
print("Current working directory:", os.getcwd())

# Make sure the logs folder exists
os.makedirs("logs", exist_ok=True)
LOG_FILE = "logs/admin_log.txt"

def log_admin_action(admin_user, command, target_user, reason):
    """Append an admin action to the local log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {admin_user} has {command} {target_user} For: {reason}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        if reason is None:
            await ctx.send("You must provide a reason. Usage: !ban @user {reason}")
            return
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned. Reason: {reason}")
        log_admin_action(ctx.author, "banned", member, reason)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = None):
        if reason is None:
            await ctx.send("You must provide a reason. Usage: !warn @user {reason}")
            return

        role_name = "Warned"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            role = await ctx.guild.create_role(name=role_name, reason="Role for warned users")

        await member.add_roles(role, reason=reason)
        await ctx.send(f"{member.mention} has been warned. Reason: {reason}")

        try:
            await member.send(f"You have been warned in **{ctx.guild.name}**. Reason: {reason}")
        except:
            pass

        log_admin_action(ctx.author, "warned", member, reason)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        if reason is None:
            await ctx.send("You must provide a reason. Usage: !mute @user {reason}")
            return

        role_name = "Muted"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            role = await ctx.guild.create_role(name=role_name, reason="Role for muted users")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False, speak=False)

        await member.add_roles(role, reason=reason)
        await ctx.send(f"{member.mention} has been muted. Reason: {reason}")

        try:
            await member.send(f"You have been muted in **{ctx.guild.name}**. Reason: {reason}")
        except:
            pass

        log_admin_action(ctx.author, "muted", member, reason)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge_user(self, ctx, member: discord.Member, *, reason: str = None):
        if reason is None:
            await ctx.send("You must provide a reason. Usage: !purge_user @user {reason}")
            return

        def is_member(m):
            return m.author == member

        deleted = await ctx.channel.purge(limit=100, check=is_member)
        await ctx.send(f"Deleted {len(deleted)} messages from {member.mention}. Reason: {reason}", delete_after=5)

        log_admin_action(ctx.author, f"purged messages of", member, reason)

async def setup(bot):
    await bot.add_cog(Admin(bot))
