import json

from discord.ext import commands


def dat():
    with open("config.json") as f:
        x = json.load(f)  # type: dict
    with open("data.json") as ff:
        y = json.load(ff)  # type:dict
    return x, y


def running(ctx: commands.Context):
    config, data = dat()
    try:
        uname = data[f"users"].get(f"{ctx.author.id}")
        return True
    except Exception as e:
        return False
