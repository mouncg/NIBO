import json

import asyncio
from discord.ext import commands
from main import NitroBot as bot


async def select(bot: bot, sql, all=False):
    while not bot.pool:
        await asyncio.sleep(0.21)
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT " + sql if not str(sql).lower().startswith("select") else sql
            )
            if all:
                return await cur.fetchall()
            return await cur.fetchone()


def dat():
    with open("config.json") as f:
        x = json.load(f)  # type: dict
    with open("data.json") as ff:
        y = json.load(ff)  # type:dict
    return x, y


async def permitted(ctx: commands.Context):
    config, data = dat()
    query = (
        f"SELECT `user_id` FROM `whitelisted_users` WHERE `user_id`='{ctx.author.id}'"
    )
    res = await select(bot=bot, sql=query)
    # return ctx.author.id in data.get("permitted_users") or ctx.author.id in config.get(
    #     "admin_ids"
    # )
    if res:
        return True
    else:
        return False


def running(ctx: commands.Context):
    config, data = dat()
    try:
        uname = data[f"users"].get(f"{ctx.author.id}")
        return True
    except Exception as e:
        return False
