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
    async def add_user(self, ctx: commands.Context, user: greedy[discord.User]):
        print(user)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"insert into whitelisted_users value {user[0].id}")
                results = await cur.fetchone()
        return await ctx.send(f"✅| {results}")


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
