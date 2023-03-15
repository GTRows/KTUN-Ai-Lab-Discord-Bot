import json
import discord
from discord.ext import commands
from discord.utils import get

import time


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # await change_status.start()
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        role = get(guild.roles, id=882942410622124053)
        await member.add_roles(role)
        channel = discord.utils.get(guild.text_channels, id=882969190565306369)
        await channel.send(f"<@!{member.id}> aramıza katıldı")
        # with open('.\\databases\\user.json', "r+") as file:
        #     data = json.load(file)
        #     time_now = "{}.{} {} {}/{}/{}".format(time.tm_hour, time.tm_min, time.tm_sec, time.tm_mday, time.tm_mon,
        #                                           time.tm_year)
        #     print(data["data"])
        #     data["data"].append({"user.author": temp, "time": time_now, "status": "member_join"})
        #     print(data["data"])
        #     file.seek(0)
        #     json.dump(data, file, ensure_ascii=False)

    # @commands.Cog.listener()
    # async def on_member_remove(self, member, time=time.localtime()):
    #     temp = str(member)
    #     with open('.\\databases\\user.json', "r+") as file:
    #         data = json.load(file)
    #         time_now = "{}.{} {} {}/{}/{}".format(time.tm_hour, time.tm_min, time.tm_sec, time.tm_mday, time.tm_mon,
    #                                               time.tm_year)
    #         data["data"].append({"user.author": temp, "time": time_now, "status": "member_removed"})
    #         file.seek(0)
    #         json.dump(data, file, ensure_ascii=False)

    # Reconnect
    @commands.Cog.listener()
    async def on_resumed(self):
        print('Bot has reconnected!')

    @commands.Cog.listener()
    async def on_disconnect(self):
        print('Bot disconnected')

    # Error Handlers
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # unknown command
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid command used.')
        # missing arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please pass in all required arguments.')

        # missing permissions
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You are missing permissions.')

        # bot missing permissions
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send('Bot is missing permissions.')

        # command on cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on a {round(error.retry_after, 2)} second cooldown.')

        # bad argument
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Invalid argument.')

        # invoke error
        elif isinstance(error, commands.CommandInvokeError):
            if "2000 or fewer" in str(error) and len(ctx.message.clean_content) > 1900:
                return await ctx.send("\n".join([
                    "You attempted to make the command display more than 2,000 characters...",
                    "Both error and command will be ignored."
                ]))
            await ctx.send(f"There was an error processing the command ;-;\n{error}")

        elif isinstance(error, commands.CheckFailure):
            pass

        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("You've reached max capacity of command usage at once, please finish the previous one...")


    @commands.Cog.listener()
    async def on_command(self, ctx):
        location_name = ctx.guild.name if ctx.guild else "Private message"
        print(f"{location_name} > {ctx.author} > {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        to_send = next((
            chan for chan in guild.text_channels
            if chan.permissions_for(guild.me).send_messages
        ), None)
        if to_send:
            await to_send.send("Hello! I'm a bot that can help you with your server. "
                               "Use `!help` to see my commands.")

async def setup(client):
    await client.add_cog(Events(client))
