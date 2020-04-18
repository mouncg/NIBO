import discord
from discord.ext import commands
from discord.ext.commands import Greedy as greedy
from main import NitroBot
import aiomysql

# yee
class OwnerCommands(commands.Cog):
    def __init__(self, bot: NitroBot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="add_user", hidden=True)
    async def add_user(self, ctx: commands.Context, user: greedy[discord.User]):
        async with self.bot.pool.acquire() as conn:
            conn = conn  # type: aiomysql.Connection
            async with conn.cursor() as cur:
                cur = cur  # type: aiomysql.Cursor
                await cur.execute(
                    # f"insert into whitelisted_users values (`{user[0].id}`)"
                    "REPLACE INTO `whitelisted_users`(`user_id`) VALUES ('{}');".format(
                        user[0].id
                    )
                )
                await conn.commit()
                conn.close()
                results = await cur.fetchone()
        if f"{results}" == f"None":
            results = f"{user[0]} has been added to the whitelisted users!"
        return await ctx.send(f" ✅| {results}")


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
