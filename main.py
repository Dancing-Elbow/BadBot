import asyncio
import datetime
import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button, button
from mongoController import MongoHelper

mongoUrl = "mongodb+srv://dancing_elbow:whtSzeK2t4ygUxHa@badbot.v3gz3ht.mongodb.net/?retryWrites=true&w=majority"
classes = {
    0: {
        "name": "Coffee Obliterator",
        "health": 100,
        "strength": 10,
        "intelligence": 10,
        "dexterity": 10,
        "mana": 10,
        "constitution": 10,
        "willpower": 10,
        "speed": 10,
        "dodge": 10,
        "critical hit chance": 10,
        "critical hit damage": 10,
        "mana regen": 10,
        "health regen": 10,

    }
}


# att * att / (att + def)
# TotalDamage = Strength * (1 + (Damage/100)) + Damage

class Game(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=discord.Intents.all(),
                         activity=discord.Game(name="With DancingElbow"))
        self.mongoDB = MongoHelper(mongoUrl)

        @self.hybrid_command(name="truth", description="reveal a truth")
        async def truth(ctx):
            await ctx.send("joe nooby")

        @self.hybrid_command(name="choose", description="choose one")
        async def choose(ctx, member: discord.Member):
            await ctx.send("your hp: 100 \nenemyhp: 100 ", view=Chooser(ctx.author, member))

        @self.hybrid_command(name="fight", description="test")
        async def fight(ctx):
            embed = discord.Embed(title="Battle Against Coffee Obliterator", color=discord.Color.og_blurple())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            embed.add_field(name=ctx.author.name, value="Health: 100")
            embed.add_field(name="Coffee Obliterator", value="Health: 100")
            embed.set_field_at(0, name="test", value="test")
            await ctx.send("your hp: 100\nenemy hp: 100", view=Fight(embed), embed=embed)

        @self.event
        async def on_message(msg):
            await msg.add_reaction('☕')

    async def on_ready(self):
        print(f"Active as {self.user.name} in {len(self.guilds)} server")

    async def setup_hook(self):
        await self.tree.sync()


class Chooser(View):
    def __init__(self, member1, member2):
        super().__init__()
        self.member1 = member1
        self.member2 = member2
        self.member_info1 = 100
        self.member_info2 = 100

    @button(label="attack the other guy", style=discord.ButtonStyle.blurple)
    async def chooser(self, interaction: discord.Interaction, button_object: Button):
        if interaction.user == self.member1:
            self.member_info2 -= 10
            await interaction.response.defer()
            await interaction.message.edit(
                content="your hp" + str(self.member_info1) + "enemyhp" + str(self.member_info2), view=self)
        else:
            await interaction.response.send_message("Wrong guy")

    @button(label="attack the guy that used the command", style=discord.ButtonStyle.red)
    async def chooser2(self, interaction: discord.Interaction, button_object: Button):
        if interaction.user == self.member2:
            self.member_info1 -= 10
            await interaction.response.defer()
            await interaction.message.edit(
                content="your hp" + str(self.member_info1) + "enemyhp" + str(self.member_info2), view=self)
        else:
            await interaction.response.send_message("Wrong guy")


class Fight(View):
    def __init__(self, embed):
        super().__init__()
        self.health1 = 100
        self.health2 = 100
        self.embed = embed

    @button(label="ATTACK", style=discord.ButtonStyle.danger)
    async def attack(self, interaction: discord.Interaction, button: discord.Button):
        self.health2 -= random.randint(10, 25)
        button.disabled = True
        if (self.health2 > 0):
            self.embed.set_field_at(0, name=self.embed.)
            await interaction.response.edit_message(embed=self.embed, view=self)
        else:
            await interaction.response.edit_message(content="YOU WIN", view=None)
            return
        await asyncio.sleep(.5)
        self.health1 -= random.randint(15, 25)
        button.disabled = False
        if (self.health1 > 0):
            await interaction.edit_original_response(
                content="your hp: " + str(self.health1) + "enemy hp: " + str(self.health2), view=self)
        else:
            await interaction.edit_original_response(content="YOU LOSE", view=None)


bot = Game()
with open("coffeeObliteratorToken.txt") as file_object:
    bot.run(file_object.readline())
