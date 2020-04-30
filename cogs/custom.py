import discord
from discord.ext import commands
from utils import colors


class custom_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="credits")
    async def credits(self, ctx: commands.Context):
        """
        Credits
        """
        e = discord.Embed(color=colors._credits())
        e.title, e.description = (
            "Credits for the bot",
            """**BOT CREATOR:**EppyPrime™#1461
            QUEUE CREATOR: adl212#2235
            
            **SUPPORT:** EppyPrime™#1461, Limt#6491
            **TRAVIS:** SOON™""",
        )
        return await ctx.send(e)


def setup(bot):
    bot.add_cog(custom_commands(bot))
