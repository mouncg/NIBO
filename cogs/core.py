import threading
from time import sleep

from discord.ext import commands
import discord
import json
from os import system
from main import NitroBot
from utils.checks import running


def data():
    with open("data.json") as f:
        config = json.load(f)  # type: dict
        return config


run = {}
money_run = {}


def runner(
    accuracy, nitroes_ammo, password, wpm, username, waittime, safe_mode, plac, uid
):
    global run
    print(run)
    while run.get(uid) is True:
        sleep(waittime)
        system(
            f"nitrous -a {accuracy} -n {nitroes_ammo} -p {password} -s 1 -w {wpm} -u {username} -t {waittime} -c 1 -S {safe_mode} -f {plac}nitro_cfg.json"
        )


class Thread(threading.Thread):
    def __init__(
        self,
        name,
        counter,
        accuracy,
        nitroes_ammo,
        password,
        wpm,
        username,
        waittime,
        safe_mode,
        plac,
        uid,
    ):

        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        self.threadID = counter
        self.name = name
        self.counter = counter
        self.accuracy = accuracy
        self.nitroes_ammo = nitroes_ammo
        self.password = password
        self.wpm = wpm
        self.username = username
        self.waittime = waittime
        self.safe_mode = safe_mode
        self.plac = plac
        self.uid = uid

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):

        print("\nStarting " + self.name)
        # Acquire lock to synchronize thread
        # threadLock.acquire()
        print(f"{self.name} [--+--] {self.counter}")
        print(f"{self.name} [--+--] started the daemon")
        runner(
            self.accuracy,
            self.nitroes_ammo,
            self.password,
            self.wpm,
            self.username,
            self.waittime,
            self.safe_mode,
            self.plac,
            self.uid,
        )
        # Release lock for the next thread
        # threadLock.release()
        print("Exiting " + self.name)


threadLock = threading.Lock()
threads = []


class Core(commands.Cog):
    """
    Core things
    """

    def __init__(self, bot):
        self.bot = bot  # type: NitroBot

    @commands.command("ping")
    async def ping(self, ctx: commands.Context):
        """
        check if the bot is online.
        """
        await ctx.send("Ping!")

    @commands.command("info")
    async def _info(self, ctx: commands.Context):
        """
        info!
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
RUNNING
```"""
            )

    @show.command(name="running")
    async def show_running(self, ctx: commands.Context):
        """
        show running bots!
        """
        config = data()
        uname = config["users"][str(ctx.author.id)]
        e = discord.Embed(color=0xFC6C85)
        e.title = f"DISCORD <=====> NITROTYPE"
        e.description = f"{uname}"
        return await ctx.send(embed=e)

    @show.command(name="password")
    async def uname(self, ctx: commands.Context):
        """
        password
        """
        config = data()
        pwd = config["account_creds"][config["users"][str(ctx.author.id)]]
        await ctx.send(f"Password for {config['users'][str(ctx.author.id)]}: ||{pwd}||")

    @commands.command(name="stop")
    @commands.check(running)
    async def _stop(self, ctx: commands.Context):
        global run, threads

        run[str(ctx.author.id)] = False
        with open("data.json") as f:
            config = json.load(f)  # type: dict
        username = config["users"].get(f"{ctx.author.id}")

        config["users"].pop(f"{ctx.author.id}", None)
        config["account_creds"].pop(f"{username}", None)
        config["info"].pop(f"{username}")
        threads = threads  # type: list
        for thread in threads:
            if thread.username == f"{username}":
                await ctx.send("The bot will stop after the race!")
                await ctx.send("The bot will take some time to kill your thread!")
                thread.stop()

                print(f"[{thread.name}] STOPPING THREAD")
                threads.remove(thread)
        with open("data.json", "w") as ff:
            json.dump(config, ff)

        return await ctx.send("FINISHED SETTING THE BOT TO KILL AFTER FINISHED RACE!")

    @commands.command(name="list_running", hidden=True)
    @commands.is_owner()
    async def _list(self, ctx: commands.Context):
        global run
        await ctx.send(f"```py\n{run}\n```")

    @commands.command(name=f"login")
    async def _login(
        self,
        ctx: commands.Context,
        username: str,
        password: str,
        wpm: int,
        accuracy: int,
    ):
        safe_mode = True
        """
        login using !login username password wpm accuracy safe_mode
        """
        user_id = ctx.author.id
        # query = (
        #     await self.bot.select(
        #         f"SELECT IFNULL((SELECT * FROM `whitelisted_users` WHERE `user_id`='{user_id}'), 0)"
        #     )
        # )[0]
        res = await self.bot.select(
            "SELECT * FROM `whitelisted_users` WHERE `user_id` is not null", all=True
        )
        # res = await self.bot.select(sql=query)
        # return ctx.author.id in data.get("permitted_users") or ctx.author.id in config.get(
        #     "admin_ids"
        # )
        # if str(user_id) not in res:
        #     return
        lst = []
        # create list of allowed
        for re in res:
            lst.append(re[0])
        print([str(ctx.author.id)])
        if str(ctx.author.id) not in lst:
            e = discord.Embed(
                color=0x64FF00,
                title=f"You do not have the permissions to run this command!",
            )
            e.set_footer(text=f"Error code 0x001")
            await ctx.send(embed=e)
            return
        if running(ctx):
            await ctx.send(
                "⚠|THE BOT IS ALREADY RUNNING! THIS COULD BREAK SOME THINGS!!!!"
            )
        global run, threads

        accuracy = float(accuracy)
        accuracy /= 100
        plac = "/home/epfforce/Programming/python/"
        nitroes_ammo = 1
        waittime = 29

        run[str(ctx.author.id)] = True
        thread1 = Thread(
            f"Thread{len(threads) + 1}",
            1,
            accuracy,
            nitroes_ammo,
            password,
            wpm,
            username,
            waittime,
            safe_mode,
            plac,
            str(ctx.author.id),
        )
        threads.append(thread1)
        thread1.setDaemon(True)
        thread1.start()
        with open("data.json") as f:
            config = json.load(f)  # type: dict
        config["users"][f"{ctx.author.id}"] = f"{username}"
        config["account_creds"][f"{username}"] = f"{password}"
        config["info"][f"{username}"] = {
            "wpm": wpm,
            "accuracy": accuracy,
            "safe_mode": safe_mode,
        }

        await ctx.send(f"Started bot {username}")
        with open("data.json", "w") as ff:
            json.dump(config, ff)


def setup(bot):
    bot.add_cog(Core(bot))
