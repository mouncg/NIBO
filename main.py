import json
from discord.ext import commands


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


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.default_prefix = "!"
with open("config.json") as f:
    bot.config = json.load(f)
    bot.owner_id = 611108193275478018
initial_extensions = ["cogs.core", "cogs.error_handler"]


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
