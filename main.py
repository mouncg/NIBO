import json

import discord
from discord.ext import commands
from os import system


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
    print("ONLINE")


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
