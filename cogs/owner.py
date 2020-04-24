import json

import discord
from discord.ext import commands
from discord.ext.commands import Greedy as greedy
from main import NitroBot
import aiomysql

# yee
class OwnerCommands(commands.Cog):
    def __init__(self, bot: NitroBot):
        self.bot = bot

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def _load(self, ctx: commands.Context, *exts):
        for i in exts:
            self.bot.load_extension(f"cogs.{i}")
            await ctx.send(f"reloaded {i}")
        await ctx.send(f"loaded {exts}")

    @commands.is_owner()
    @commands.command(name="add_user", hidden=True)
    async def add_user(self, ctx: commands.Context, user: greedy[discord.User]):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
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

    @commands.command(name="reload_config")
    @commands.is_owner()
    async def _reload_cfg(self, ctx: commands.Context):
        with open("config.json") as f:
            self.bot.config = json.load(f)
            self.bot.owner_ids = self.bot.config["admin_ids"]

    @commands.is_owner()
    @commands.command(name="del_user", hidden=True)
    async def del_user(self, ctx: commands.Context, user: greedy[discord.User]):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "delete from whitelisted_users where user_id = {}".format(
                        user[0].id
                    )
                )
                await conn.commit()
                conn.close()
                results = await cur.fetchone()
        if f"{results}" == f"None":
            results = f"{user[0]} has been removed from the whitelisted users!"
        return await ctx.send(f" ✅| {results}")


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
