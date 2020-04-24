import json

import aiohttp
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
    @commands.has_role(696844654569717761)
    async def _load(self, ctx: commands.Context, *exts):
        for i in exts:
            self.bot.load_extension(f"cogs.{i}")
            await ctx.send(f"reloaded {i}")
        await ctx.send(f"loaded {exts}")

    @commands.has_role(696844654569717761)
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

    @commands.command(name="reload_config", hidden=True)
    @commands.has_role(696844654569717761)
    async def _reload_cfg(self, ctx: commands.Context):
        with open("config.json") as f:
            self.bot.config = json.load(f)
            self.bot.owner_ids = {
                611108193275478018,
                611276921832996876,
                702870297384058911,
                645415863767531541,
            }
        await ctx.send("RELOADED!")

    @commands.has_role(696844654569717761)
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

    @commands.command(name="", hidden=True)
    @commands.has_role(696844654569717761)
    async def test(self, ctx: commands.Context):
        async def fetch(session, url, data):
            async with session.post(url, data=data) as response:
                return await response.json()

        async def chk(username, password):
            async with aiohttp.ClientSession() as session:
                html = await fetch(
                    session,
                    "https://www.nitrotype.com/api/login",
                    {"username": username, "password": password},
                )
                html = str(html).split(",")
                html = html[0]
                html = html.split(":")
                html = html[1]
                html = html.replace(" ", "")
                await ctx.send(f"```{html}```")

        await chk("rip21219", "rip212w19")


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
