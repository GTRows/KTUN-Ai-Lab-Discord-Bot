import asyncio
import random

import discord
from discord.ext import commands


class FunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["howhot", "hot"])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """
        Returns a random percent for how hot is a discord user

        :param user: The user to check
        """
        user = user or ctx.author
        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17
        match hot:
            case x if x > 75:
                emoji = "💞"
            case x if x > 50:
                emoji = "💖"
            case x if x > 25:
                emoji = "❤"
            case _:
                emoji = "💔"
        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(aliases=["slots", "bet"])
    async def slot(self, ctx):
        """ Slot machine game """
        a, b, c = [random.choice("🍎🍊🍐🍋🍉🍇🍓🍒") for _ in range(3)]
        if (a == b == c):
            results = "All matching, you won! 🎉"
        elif (a == b) or (a == c) or (b == c):
            results = "2 in a row, you won! 🎉"
        else:
            results = "No match, you lost 😢"

        await ctx.send(f"**[ {a} {b} {c} ]\n{ctx.author.name}**, {results}")

    @commands.command()
    async def dice(self, ctx, *, user: discord.Member = None):
        """ Dice game. Good luck """
        if user:
            if user == ctx.author:
                return await ctx.send("You can't play with yourself")

        bot_dice, player_dice = [random.randint(1, 6) for g in range(2)]

        match player_dice:
            case x if x > bot_dice:
                final_message = "Congrats, you won 🎉"
            case x if x < bot_dice:
                final_message = "You lost, try again... 🍃"
            case _:
                final_message = "It's a tie 🎲"

        if user == self.client.user:
            results = "\n".join([
                f"**{self.client.user.display_name}:** 🎲 {bot_dice}",
                f"**{ctx.author.display_name}** 🎲 {player_dice}"
            ])
            await ctx.send(f"{results}\n> {final_message}")
        elif user:
            results = "\n".join([
                f"**{ctx.author.display_name}:** 🎲 {player_dice}",
                f"**{user.display_name}** 🎲 {bot_dice}"
            ])
            await ctx.send(f"{results}\n> {final_message}")
        else:
            results = f"**{ctx.author.display_name}** 🎲 {player_dice}"
            await ctx.send(f"{results}")

    @commands.command(aliases=['colors'])
    async def roulette(self, ctx, picked_colour: str = None):
        """ Colours roulette """
        colour_table = ["blue", "red", "green", "yellow"]
        if not picked_colour:
            pretty_colours = ", ".join(colour_table)
            return await ctx.send(f"Please pick a colour from: {pretty_colours}")

        picked_colour = picked_colour.lower()
        if picked_colour not in colour_table:
            return await ctx.send("Please give correct color")

        chosen_color = random.choice(colour_table)
        msg = await ctx.send("Spinning 🔵🔴🟢🟡")
        await asyncio.sleep(1)
        result = f"Result: {chosen_color.upper()}"

        if chosen_color == picked_colour:
            await msg.edit(content=f"> {result}\nCongrats, you won 🎉!")
        else:
            await msg.edit(content=f"> {result}\nBetter luck next time")


async def setup(client):
    await client.add_cog(FunCog(client))
