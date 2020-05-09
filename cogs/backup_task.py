import datetime
import json

from discord.ext import commands, tasks
import discord
from main import NitroBot


class Backups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # type: NitroBot

    @tasks.loop(minutes=30)
    async def data_backup(self):
        with open("data.json") as f:
            data = json.load(f)
        with open(f"backups/data/{datetime.datetime}.json", "w") as f:
            json.dump(data, f)

    @tasks.loop(minutes=10)
    async def running_backup(self):
        with open("spd.txt") as f:
            data = json.load(f)
        with open(f"backups/running/{datetime.datetime}.txt") as f:
            json.dump(data, f)

    @data_backup.after_loop
    async def _done_main_backup(self):
        await self.bot.get_channel(708675580803022948).send(
            embed=discord.Embed(
                color=0x64FF00,
                name="BACKUP FINISHED",
                description="The data backup has finished!",
            )
        )

    @running_backup.after_loop
    async def _done_running_backup(self):
        await self.bot.get_channel(708675580803022948).send(
            embed=discord.Embed(
                color=0x64FF00,
                name="BACKUP FINISHED",
                description="The running backup has finished!",
            )
        )

    @commands.command(name="start_loop")
    async def start_backups(self, ctx):
        try:
            self.running_backup.start()
            self.data_backup.start()
        except RuntimeError as e:
            await ctx.send(e)

    @commands.Cog.listener(name="on_ready")
    async def start_backups(self):
        self.running_backup.start()
        self.data_backup.start()


def setup(bot: NitroBot):
    bot.add_cog(Backups(bot))
