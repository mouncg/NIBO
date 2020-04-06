import asyncio
from datetime import datetime
import json
import traceback

import aiomysql
import discord
from cprint import cprint
from discord.ext import commands
from os import system

# yeet
from pymysql import OperationalError

import outh


def get_config():
    with open("config.json") as f:
        return json.load(f)


def get_prefix(bot, msg):
    cfg = get_config()  # type: dict
    if not msg.guild:
        return commands.when_mentioned_or(bot.default_prefix)(bot, msg)
    guild_id = str(msg.guild.id)
    if "prefix" not in cfg:
        cfg["prefix"] = {}
    prefixes = cfg["prefix"]
    if guild_id not in prefixes:
        return commands.when_mentioned_or(bot.default_prefix)(bot, msg)
    return commands.when_mentioned_or(prefixes[guild_id])(bot, msg)


class NitroBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(
            command_prefix=get_prefix,
            activity=discord.Game(name="Yeeting NitroType"),
            **options,
        )
        self.pool = None  # MySQL Pool initialized on_ready
        self.logs = []

    async def create_pool(self):
        sql = outh.MySQL()
        try:
            self.pool = await aiomysql.create_pool(
                host=sql.host,
                port=sql.port,
                user=sql.user,
                password=sql.password,
                db=sql.db,
                loop=self.loop,
                minsize=10,
                maxsize=64,
            )
        except (ConnectionRefusedError, OperationalError):
            self.log(
                "Couldn't connect to SQL server", "CRITICAL", tb=traceback.format_exc()
            )
            self.log("Logging out..")
            await self.logout()
        else:
            self.log(f"Initialized db {sql.db} with {sql.user}@{sql.host}")

    async def insert(self, table, *values):
        while not self.pool:
            await asyncio.sleep(0.21)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                command = f"INSERT INTO {table} VALUES ({', '.join([str(v) for v in values])});"
                await cur.execute(command)
                await conn.commit()

    async def select(self, sql, all=False):
        while not self.pool:
            await asyncio.sleep(0.21)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT " + sql
                    if not str(sql).lower().startswith("select")
                    else sql
                )
                if all:
                    return await cur.fetchall()
                return await cur.fetchone()

    async def update(self, table, **where):
        while not self.pool:
            await asyncio.sleep(0.21)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                set_key, set_value = list(where.items())[0]
                command = f"UPDATE {table} SET {set_key} = {set_value}"
                for i, (key, value) in enumerate(where.items()):
                    if i == 0:
                        continue
                    if i == 1:
                        command += f" WHERE {key} = {value}"
                    else:
                        command += f" and {key} = {value}"
                await cur.execute(command + ";")
                await conn.commit()

    def log(self, message, level="INFO", tb=None, color=None):
        if level == "DEBUG" and not self.debug_mode:
            return
        now = str(datetime.now().strftime("%I:%M%p"))
        if now.startswith("0"):
            now = now.replace("0", "", 1)
        lines = []
        for line in message.split("\n"):
            msg = f"{now} | {level} | {line}"
            if level == "DEBUG" and self.config["debug_mode"]:
                if color:
                    cprint(msg, color)
                else:
                    cprint(msg, "cyan")
            elif level == "INFO":
                if color:
                    cprint(msg, color)
                else:
                    cprint(msg, "green")
            elif level == "CRITICAL":
                if color:
                    cprint(msg, color)
                else:
                    cprint(msg, "red")
            lines.append(msg)
        if tb:
            if color:
                cprint(str(tb), color)
            else:
                cprint(str(tb), "red")
            lines.append(str(tb))
        self.logs.append("\n".join(lines))
        self.logs = self.logs[:1000]


bot = NitroBot()
bot.default_prefix, bot.description = (
    "!",
    f"This bot is to cheat on the web game Nitrotype (https://nitrotype.com) "
    f"and will allow you to yeet people and gain moneyyyz",
)
with open("config.json") as f:
    bot.config = json.load(f)
    bot.owner_id = 611108193275478018
initial_extensions = ["cogs.core", "cogs.error_handler", "cogs.owner"]


def load_exts(bot):
    for ext in initial_extensions:
        try:
            bot.load_extension(f"{ext}")
            print(f"loaded {ext}")
        except Exception as e:
            print(e)


@bot.listen("on_ready")
async def ONLINE():
    print("THE BOT IS ONLINE")


@bot.listen(name="on_ready")
async def mysql_init():
    await bot.create_pool()
    print(f"STARTED MYSQL")


@bot.command(name="inst_req", hidden=True)
@commands.is_owner()
async def _inst(ctx: commands.Context):
    system("npm i @ifvictr/nitrous")


@bot.command(name="reload", hidden=True)
@commands.is_owner()
async def _reload(ctx: commands.Context, *exts):
    for i in exts:
        bot.reload_extension(f"cogs.{i}")
        await ctx.send(f"reloaded {i}")
    await ctx.send(f"reloaded {exts}")


@bot.command("testbot")
@commands.is_owner()
async def testbot(ctx: commands.Context):
    await ctx.send("Sup, I am online!")


if __name__ == "__main__":
    load_exts(bot)
    bot.run(bot.config["token"])
