import discord
from discord.ext import commands
from discord.ext.commands import Greedy as greedy

# yee
class OwnerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="add_user")
    async def add_user(self, ctx: commands.Context, user: greedy[discord.User]):
        return ctx.send("Yeet")


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
