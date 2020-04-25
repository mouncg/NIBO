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
        with open("config.json") as f:
            self.config = json.load(f)

    @commands.command(name="load", hidden=True)
    @commands.has_role(696844654569717761)
    async def _load(self, ctx: commands.Context, *exts):
        for i in exts:
            self.bot.load_extension(f"cogs.{i}")
            await ctx.send(f"reloaded {i}")
        await ctx.send(f"loaded {exts}")

    @commands.command(
        name="MRA",
        aliases=["massroleadd", "mass_role_add", "mass-role-add"],
        hidden=True,
    )
    @commands.has_role(696844654569717761)
    async def _MRA(self, ctx: commands.Context):
        for member in ctx.guild.members:
            member = member  # type: discord.Member
            g = ctx.guild  # type: discord.Guild
            crm = self.config.get("runner_role_id")

            await member.add_roles(g.get_role(crm), reason="MRA")

    @commands.command(name="test", hidden=True)
    @commands.has_role(696844654569717761)
    async def test(self, ctx: commands.Context):
        return await ctx.send("OwO, DISABLED")

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
