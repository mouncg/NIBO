from discord.ext import commands
import discord
import json
from os import system
from utils.checks import permitted


def data():
    with open("data.json") as f:
        config = json.load(f)  # type: dict
        return config


class Core(commands.Cog):
    """

    """

    def __init__(self, bot):
        self.bot = bot  # type: commands.Bot

    @commands.command("ping")
    async def ping(self, ctx: commands.Context):
        """
        check if the bot is online.
        :param ctx:
        """
        await ctx.send("Ping!")

    @commands.command("info")
    async def _info(self, ctx: commands.Context):
        """
        info!
        :param ctx:
        :return:
        """
        config = data()
        users = config["users"]  # type: dict
        info = config["info"]
        if str(ctx.author.id) in config["users"]:
            for user in users:
                username = users.get(user)
                info = info[username]
                uinfo = {
                    "username": username,
                    "wpm": info["wpm"],
                    "accuracy": info["accuracy"],
                    "safe": info["safe_mode"],
                }
                e = discord.Embed(color=0x64FF00)
                e.title = f"NITROTYPE BOT"
                e.add_field(name=f"USERNAME", value=f'{uinfo.get("username")}')
                e.add_field(name="\u200b", value="\u200b")
                e.add_field(name=f"WPM", value=f'{uinfo.get("wpm")}')
                e.add_field(name=f"accuracy", value=f'{uinfo.get("accuracy") * 100}')
                e.add_field(name="\u200b", value="\u200b")
                e.add_field(name=f"Safe Mode", value=f'{uinfo.get("safe")}')
                await ctx.send(embed=e)
        else:
            await ctx.send(
                "You are not logged in with any accounts.\nto log in please use `!login` and follow the "
                "instructions."
            )

    @commands.group(name="show")
    async def show(self, ctx: commands.Context):
        """
        show info, useful for troubleshooting, shows private info.
        :param ctx:
        :return:
        """
        config = data()
        users = config["users"]  # type: dict
        info = config["info"]
        if str(ctx.author.id) not in config["users"]:
            return await ctx.send("Please start the bot to see this info.")
        if ctx.subcommand_passed is None or ctx.invoked_subcommand == "":

            await ctx.send(
                f"""```
PASSWORD
```"""
            )

    @show.command(name="password")
    async def uname(self, ctx: commands.Context):
        """
        password
        :param ctx:
        """
        config = data()
        pwd = config["account_creds"][config["users"][str(ctx.author.id)]]
        await ctx.send(f"Password for {config['users'][str(ctx.author.id)]}: ||{pwd}||")

    @commands.command(name=f"login")
    @commands.check(permitted)
    @commands.dm_only()
    async def _login(
        self,
        ctx: commands.Context,
        username: str,
        password: str,
        wpm: int,
        accuracy: int,
        safe_mode: bool,
    ):
        """
        login!
        :param ctx:
        :param username:
        :param password:
        :param wpm:
        :param accuracy:
        :param safe_mode:
        :return:
        """
        accuracy = float(accuracy)
        accuracy /= 100
        plac = "/home/epfforce/Programming/"
        nitroes_ammo = 1
        waittime = 64
        print(
            system(
                f"screen -d -m -L nitrous -a {accuracy} -n {nitroes_ammo} -p {password} -s 1 -w {wpm} -u {username} -t {waittime} -S {safe_mode} -f {plac}nitro_cfg.json"
            )
        )
        with open("data.json") as f:
            config = json.load(f)  # type: dict
        config["users"][f"{ctx.author.id}"] = f"{username}"
        config["account_creds"][f"{username}"] = f"{password}"
        config["info"][f"{username}"] = {
            "wpm": wpm,
            "accuracy": accuracy,
            "safe_mode": True,
        }

        await ctx.send(f"Started bot {username}")
        with open("data.json", "w") as ff:
            cf = config
            # cf = str(cf).replace("'", '"').replace(True, 'true')
            # ff.writelines(f"""{cf}""")
            json.dump(config, ff)


def setup(bot):
    bot.add_cog(Core(bot))
