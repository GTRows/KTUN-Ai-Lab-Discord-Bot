import asyncio
import json
import discord
from discord.ext import commands
from discord.utils import get

import time


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("member joined")
        print("Member joined the server: " + member.name + " at " + time.strftime("%H:%M:%S"))
        guild = member.guild
        role = get(guild.roles, id=882942410622124053)
        await member.add_roles(role)
        time_now = "{}.{} {} {}/{}/{}".format(time.tm_hour, time.tm_min, time.tm_sec, time.tm_mday, time.tm_mon,
                                              time.tm_year)
        data = ({"user.author": str(member), "time": time_now, "status": "member_join"})

    @commands.Cog.listener()
    async def on_member_remove(self, member, time=time.localtime()):
        print("member left")
        print("Member left the server: " + member.name + " at " + time.strftime("%H:%M:%S"))
        time_now = "{}.{} {} {}/{}/{}".format(time.tm_hour, time.tm_min, time.tm_sec, time.tm_mday, time.tm_mon,
                                              time.tm_year)
        data = ({"user.author": str(member), "time": time_now, "status": "member_removed"})


    # Reconnect
    @commands.Cog.listener()
    async def on_resumed(self):
        print('Bot has reconnected!')

    @commands.Cog.listener()
    async def on_disconnect(self):
        print('Bot disconnected')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        location_name = ctx.guild.name if ctx.guild else "Private message"
        print(f"{location_name} > {ctx.author} > {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.channel.id == 1079883041398333460:
            await asyncio.sleep(5)
            await message.delete()


async def setup(client):
    await client.add_cog(Events(client))
