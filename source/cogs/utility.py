from discord.ext import commands
import discord

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        """Shows info about the server."""
        guild = ctx.guild
        embed = discord.Embed(title=f"{guild.name}", color=discord.Color.green())
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
        await ctx.send(embed=embed)

    @commands.command()
    async def poll(self, ctx, *, args):
        """Create a simple reaction poll (max 10 options)."""
        # Split by | to separate question from options
        parts = args.split("|")
        if len(parts) < 2:
            await ctx.send("Format: !poll question | option1 | option2 | ...")
            return

        question = parts[0].strip()
        options = [o.strip() for o in parts[1:]]
        if len(options) > 10:
            await ctx.send("Max 10 options allowed.")
            return

        description = ""
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for i, option in enumerate(options):
            description += f"{emojis[i]} {option}\n"

        embed = discord.Embed(title=question, description=description)
        msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await msg.add_reaction(emojis[i])


async def setup(bot):
    await bot.add_cog(Utility(bot))
