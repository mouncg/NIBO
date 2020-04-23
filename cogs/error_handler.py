import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        print(f"{error}")
        await ctx.message.add_reaction("❌")
        await self.bot.get_channel(702987609575522330).send(f"{error}")

        if isinstance(error, commands.MissingRequiredArgument):
            if f"{error}" == f"safe_mode is a required argument that is missing.":
                await ctx.send("SET this to `True`/`False`!")
            else:
                await ctx.send(f"{error}")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
