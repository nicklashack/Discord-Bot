from discord.ext import commands
import discord
import json
import os

DATA_FILE = "verification.json"

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        # Load existing JSON data
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                print("verification.json is empty or invalid. Initializing empty dict.")
                self.data = {}
        print("Verification data loaded:", self.data)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_rules(self, ctx, role: discord.Role):
        """
        Sets up a rules message with reaction.
        Users who react get the specified role.
        """
        embed = discord.Embed(
            title="Server Rules",
            description="React with ✅ to agree to the rules and get access!",
            color=discord.Color.blue()
        )
        rules_message = await ctx.send(embed=embed)
        await rules_message.add_reaction("✅")

        # Store guild data
        self.data[str(ctx.guild.id)] = {
            "message_id": rules_message.id,
            "role_id": role.id
        }
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f)
        #await ctx.send("Rules setup complete!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Assign role when a user reacts with ✅ to the rules message."""
        guild_data = self.data.get(str(payload.guild_id))
        if not guild_data:
            return
        if payload.message_id != guild_data["message_id"]:
            return
        if str(payload.emoji) != "✅":
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            print("Guild not found.")
            return

        try:
            member = await guild.fetch_member(payload.user_id)
            role = guild.get_role(guild_data["role_id"])
            bot_member = guild.me

            print(f"Bot top role: {bot_member.top_role.name}")
            print(f"Target role: {role.name}")
            print(f"Assigning role to: {member.name}")

            if member and role:
                await member.add_roles(role, reason="Agreed to rules")
                print(f"Successfully gave role {role.name} to {member.name}")
        except Exception as e:
            print("Error assigning role:", e)

async def setup(bot):
    await bot.add_cog(Verification(bot))
