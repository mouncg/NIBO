import threading
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
import aiohttp
import asyncio
from discord.ext import commands
import discord
import json
from os import system
from main import NitroBot
from utils.checks import running
import ast
import random

unb = []
idb = []

queue = asyncio.Queue()


async def worker(q: asyncio.Queue):
    global threads, uLock, tasks
    while True:
        xfn = await q.get()  # type: Thread
        print("x")
        uLock[f"{xfn.uid}"] = False
        if run.get(xfn.uid) is True:
            print("y")
            # Get a "work item" out of the queue.

            # Sleep for the "sleep_for" seconds.
            if xfn.stopped():
                xfn.start()
                threads.append(xfn)

                # Notify the queue that the "work item" has been processed.
                q.task_done()
                q.put_nowait(xfn)
            else:
                print(f"Running?\nproc syst:{xfn}\n{xfn.stopped()}")


def data():
    with open("data.json") as f:
        config = json.load(f)  # type: dict
        return config


def cfg():
    with open("config.json") as f:
        return json.load(f)


uLock = {}
run = {}
money_run = {}
gruns = 0
loop = asyncio.get_event_loop()
# executor = ThreadPoolExecutor(max_workers=30)

ldw = False


def runner(
    accuracy, nitroes_ammo, password, wpm, username, waittime, safe_mode, plac, uid, q,
):
    global uLock
    if uLock[f"{uid}"]:
        pass
    else:
        waittime = random.randint(5, waittime)
        TCN = 1
        frn = True

        rngb = random.randint(450, 670)
        if TCN % rngb == 0:
            rnga = random.randint(30, 60)
            sleep(60 * rnga)
        sleep(waittime)
        rxpl = (
            "".join(random.randint(1, 10000))
            .replace("1", "a")
            .replace("2", "b")
            .replace("3", "c")
            .join(".log")
        )
        system(
            f"nitrous -a {accuracy} -n {nitroes_ammo} -p {password} -s 2 -w {wpm} -u {username} -t {waittime} -c 5 -S {safe_mode} -f {plac}nitro_cfg.json >> {rxpl}"
        )
        TCN += 1
        if frn:
            frn = False
        q.task_done()


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
        queue,
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
        self.queue = queue

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        print("\nStarting " + self.name)
        # Acquire lock to synchronize thread
        # threadLock.acquire()
        print(f"{self.name} [--+--] {self.counter}")
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
            self.queue,
        )
        # Release lock for the next thread
        # threadLock.release()
        print("Exiting " + self.name)


threadLock = threading.Lock()
threads = []


async def fetch(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.json()


# async def arunner(
#     accuracy, nitroes_ammo, password, wpm, username, waittime, safe_mode, plac, uid
# ):
#     global run
#     print(run)
#     while run.get(uid) is True:
#         sleep(waittime)
#         system(
#             f"nitrous -a {accuracy} -n {nitroes_ammo} -p {password} -s 1 -w {wpm} -u {username} -t {waittime} -c 1 -S {safe_mode} -f {plac}nitro_cfg.json"
#         )


class Core(commands.Cog):
    """
    Core things
    """

    def __init__(self, bot):
        self.bot = bot  # type: NitroBot

    @commands.Cog.listener(name="on_ready")
    async def load_blacklists(self):
        """
        blacklist users from using the bot :rofl:
        """
        global idb, unb
        with open("id_blacklist.txt") as f:
            idb = ast.literal_eval(f"{f.readline()}")
        with open("username_blacklist.txt") as ff:
            unb = ast.literal_eval(f"{ff.readline()}")

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

    @commands.command(name="stop")
    @commands.check(running)
    async def _stop(self, ctx: commands.Context):
        global run, threads, ldw
        if ldw is False:
            return await ctx.send(
                "WE ARE CURRENTLY DISABLING THE SERVICE FOR MAINTENANCE, TRY AGAIN LATER!"
            )

        run[str(ctx.author.id)] = False
        with open("data.json") as f:
            config = json.load(f)  # type: dict
        username = config["users"].get(f"{ctx.author.id}")

        config["users"].pop(f"{ctx.author.id}", None)
        config["account_creds"].pop(f"{username}", None)
        config["info"].pop(f"{username}")
        threads = threads  # type: # list
        for thread in threads:
            if thread.username == f"{username}":
                thread.stop()

                print(f"[{thread.name}] STOPPING THREAD")
                threads.remove(thread)
        with open("data.json", "w") as ff:
            json.dump(config, ff)

        return await ctx.send("FINISHED SETTING THE BOT TO KILL AFTER FINISHED RACE!")

    @commands.command(name="list_running", hidden=True)
    @commands.has_role(696844654569717761)
    async def _list(self, ctx: commands.Context):
        global run
        with open("spd.txt", "w") as f:
            f.write(str(run))
        file = discord.File("spd.txt", filename="running_users.json")
        await ctx.send(file=file)

    @commands.command(name="SP")
    @commands.has_role(696844654569717761)
    async def _sp(self, ctx: commands.Context):
        global run
        with open("spd.txt", "w") as f:
            f.write(str(run))
        await ctx.send("SAVED!")

    @commands.command(
        name="FSP", hidden=True,
    )
    @commands.has_role(696844654569717761)
    async def _FSP(self, ctx: commands.Context, user: commands.Greedy[discord.User]):
        user = user[0]
        global run, threads, gruns
        run[str(user.id)] = False
        with open("data.json") as f:
            config = json.load(f)  # type: dict
        username = config["users"].get(f"{user.id}")

        config["users"].pop(f"{ctx.author.id}", None)
        config["account_creds"].pop(f"{username}", None)
        config["info"].pop(f"{username}")
        threads = threads  # type: # list
        for thread in threads:
            if thread.username == f"{username}":
                thread.stop()

                print(f"[{thread.name}] STOPPING THREAD")
                threads.remove(thread)
        with open("data.json", "w") as ff:
            json.dump(config, ff)
        gruns -= 1
        return await ctx.send("FINISHED SETTING THE BOT TO KILL AFTER FINISHED RACE!")

    @commands.command(name="blacklist_discord")
    @commands.has_role(696844654569717761)
    async def _blacklist_dsc(
        self, ctx: commands.Context, user: commands.Greedy[discord.User]
    ):
        global idb
        if user in idb:
            idb.remove(user)
            m = f"UNBLACKLISTED {user}"
        else:
            idb.append(user)
            m = f"BLACKLISTED {user}"
        await ctx.send(f"{m}")
        with open("id_blacklist.txt", "w") as f:
            f.write(str(idb))
        await ctx.send("SAVED USER BLACKLIST!")

    @commands.command(name="blacklist_username")
    @commands.has_role(696844654569717761)
    async def _blacklist_unb(self, ctx: commands.Context, user: str):
        global unb
        if user in unb:
            unb.remove(user)
            m = f"UNBLACKLISTED {user}"
        else:
            unb.append(user)
            m = f"BLACKLISTED {user}"
        await ctx.send(f"{m}")
        with open("username_blacklist.txt", "w") as f:
            f.write(str(unb))
        await ctx.send("SAVED USER BLACKLIST!")

    @commands.command(name="ldw")
    @commands.has_role(696844654569717761)
    async def _ldw(self, ctx: commands.Context):
        global ldw
        if ldw:
            ldw = False
            m = "BLOCKED LOGGING IN!"
        else:
            ldw = True
            m = "ENABLED LOGGING IN!"
        return await ctx.send(m)

    @commands.command(name="proc")
    @commands.has_role(696844654569717761)
    async def _proc(self, ctx: commands.Context):
        global queue
        tasks = []
        if queue.qsize() < 30:
            for i in range(queue.qsize()):
                task = asyncio.create_task(worker(queue))
                tasks.append(task)
        else:
            for i in range(30):
                task = asyncio.create_task(worker(queue))
                tasks.append(task)
        await ctx.send("Proc started")

    @commands.command(name="LD")
    @commands.has_role(696844654569717761)
    async def _ld(self, ctx: commands.Context):
        global run, threads, ldw, gruns, idb, unb, queue
        ldw = False
        with open("spd.txt") as f:
            r = ast.literal_eval(f"{f.readline()}")
        run = r  # type: dict
        for key in run.items():
            try:
                if run[key[0]] is True:
                    if int(key[0]) in idb:
                        return
                    await ctx.send(f"STARTING {key[0]}")
                    dat = data()
                    uname = dat["users"][key[0]]
                    if uname in unb:
                        return
                    password = dat["account_creds"].get(uname)
                    accuracy = dat["info"][uname].get("accuracy")
                    safe_mode = dat["info"][uname].get("safe_mode")
                    wpm = dat["info"][uname].get("wpm")
                    if accuracy >= 97:
                        accuracy = 97
                        await ctx.send("ACCURACY IS TOO HIGH, CHANGED TO 97!")
                    if wpm >= 111:
                        wpm = 70
                        await ctx.send("WPM IS TOO HIGH, LOADED TO 70!")
                    nitroes_ammo = 1
                    waittime = 29
                    plac = "/home/epfforce/Programming/python/"
                    thread = Thread(
                        f"Thread{len(threads) + 1}",
                        1,
                        accuracy,
                        nitroes_ammo,
                        password,
                        wpm,
                        uname,
                        waittime,
                        safe_mode,
                        plac,
                        str(ctx.author.id),
                        queue,
                    )

                    thread.daemon = False
                    gruns += 1
            except Exception as e:
                await self.bot.get_channel(704291784565456906).send(f"{e}")
                r[key[0]] = False
                pass
        with open("spd.txt", "w") as f:
            f.write(str(run))
        ldw = True
        run = r

    @commands.dm_only()
    @commands.command(name=f"login")
    async def _login(
        self,
        ctx: commands.Context,
        username: str = None,
        password: str = None,
        wpm: int = None,
        accuracy: int = None,
    ):
        global run, threads, ldw, gruns, queue, unb, idb, uLock
        if ldw is False:
            return await ctx.send(
                "WE ARE CURRENTLY DISABLING THE SERVICE FOR MAINTENANCE, TRY AGAIN LATER!"
            )

        if (
            username is None or password is None or wpm is None or accuracy is None
        ):  # KEEP AT FRONT OF THE CODE
            return await ctx.send(
                f"THE USAGE FOR THIS COMMAND IS `!login <username> <password> <wpm> <accuracy>`, please use this "
                f"without the `<>` part! "
            )
        if accuracy >= 97:
            accuracy = 97
            await ctx.send("ACCURACY IS TOO HIGH, CHANGED TO 97!")
        if wpm >= 111:
            wpm = 70
            await ctx.send("WPM IS TOO HIGH, LOADED TO 70!")
        if wpm > 40:
            wpm -= 20
        if 40 > wpm > 5:
            wpm -= 5
        if username in unb or ctx.author.id in idb:
            return await ctx.send("YOU ARE BLACKLISTED! PLEASE DON'T DO THIS!")
        safe_mode = True
        with open("data.json") as f:
            c = json.load(f)  # type: dict
        # try:
        #     if c["users"][f"{ctx.author.id}"]:
        #         if c["users"][f"{ctx.author.id}"] == f"{username}":
        #             return await ctx.send(
        #                 f"THE BOT IS ALREADY RUNNING ON THIS ACCOUNT! PLEASE DO `!stop` TO"
        #                 f" STOP THE BOT AND RESTART IT TO CHANGE THE SETTINGS!"
        #             )
        # except KeyError:
        #     pass
        """
        login using !login username password wpm accuracy
        """
        uid = ctx.author.id
        guild = self.bot.get_guild(695056476754018394)  # type: discord.Guild
        cmbr = guild.get_member(uid)  # type: discord.Member
        lng = len(cmbr.roles)
        lng1 = 0
        config = cfg()
        for role in cmbr.roles:
            role = role  # type: discord.Role
            if str(role.id) != str(config.get("runner_role_id")):
                if lng1 == lng - 1:
                    e = discord.Embed(
                        color=0x64FF00,
                        title=f"You do not have the permissions to run this command!",
                    )
                    e.set_footer(text=f"Error code 0x001")
                    return await ctx.send(embed=e)
            else:
                break
            lng1 += 1
        if running(ctx):
            await ctx.send(
                "⚠|THE BOT IS ALREADY RUNNING! THIS COULD BREAK SOME THINGS!!!!"
            )

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
        if html != "True":
            return await ctx.send("INCORRECT USERNAME/PASSWORD!")

        accuracy = float(accuracy)
        accuracy /= 100
        plac = "/home/epfforce/Programming/python/"
        nitroes_ammo = 1
        waittime = 29

        run[str(ctx.author.id)] = True
        uLock[f"{ctx.author.id}"] = True
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
            queue,
        )
        queue.put_nowait(thread1)
        gruns += 1
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
