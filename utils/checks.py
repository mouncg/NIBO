import json

from discord.ext import commands


def dat():
    with open("config.json") as f:
        x = json.load(f)  # type: dict
    with open("data.json") as ff:
        y = json.load(ff)  # type:dict
    return x, y


def permitted(ctx: commands.Context):
    config, data = dat()
    return ctx.author.id in data.get("permitted_users") or ctx.author.id in config.get(
        "admin_ids"
    )
