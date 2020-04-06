import discord
from discord.ext import commands
from discord.ext.commands import Greedy as greedy
from main import NitroBot

# yee
class OwnerCommands(commands.Cog):
    def __init__(self, bot: NitroBot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="add_user")
    async def add_user(self, ctx: commands.Context, users: greedy[discord.User]):
        results = []
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                for user in users:
                    await cur.execute(
                        f"insert into whitelisted_users values ('{user.id}')"
                    )
                    res = await cur.fetchone()
                    results.append(res)
        if f"{results}" == f"None":
            userStr = ""
            for _ in users:
                userStr += f"{_},"
            results = f"{userStr} has been added to the whitelisted users!"
        return await ctx.send(f"✅| {results}")


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
