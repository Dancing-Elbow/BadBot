import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View


class Game(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=discord.Intents.all(),
                         activity=discord.Game(name="With DancingElbow"))

        @self.hybrid_command(name="truth", description="reveal a truth")
        async def truth(ctx):
            await ctx.send("joe nooby")

        @self.event
        async def on_message(msg):
            await msg.add_reaction('☕')

    async def on_ready(self):
        print(f"Active as {self.user.name} in {len(self.guilds)} server")

    async def setup_hook(self):
        await self.tree.sync()



bot = Game()
with open("token.txt") as file_object:
    bot.run(file_object.readline())

