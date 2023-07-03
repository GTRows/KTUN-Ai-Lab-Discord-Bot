import discord
import asyncio
import os
import sys
import traceback
import logging
import aiohttp
from discord.ext import commands
from itertools import cycle
from discord.ext.commands import ExtensionFailed, ExtensionNotFound, NoEntryPointError
from dotenv import load_dotenv
from discord import app_commands


class KtunAiLabBot(commands.Bot):
    bot_app_info: discord.AppInfo
    bot_prefix = '!'
    bot_version = '0.5'

    # Gateway intents
    intents = discord.Intents.all()
    intents.members = True
    intents.presences = True
    intents.message_content = True



    def __init__(self):
        super().__init__(command_prefix=self.bot_prefix, intents=self.intents)
        self.session: aiohttp.ClientSession = None
        load_dotenv(dotenv_path="config/.env", verbose=True)



    async def start(self, debug: bool = False, reconnect: bool = True) -> None:
        self.debug = debug
        print(f"Bot version: {self.bot_version}")
        print(f"Bot prefix: {self.bot_prefix}")
        if self.debug:
            print("Debug mode enabled")
            await super().start(os.getenv('TOKEN'), reconnect=reconnect)
        else:
            await super().start(os.getenv('TOKEN'), reconnect=reconnect)
        # bot start call setup_hook
        await self.tree.copy_global_to()
        await self.tree.sync()

    async def setup_hook(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()
        if self.owner_id:
            self.owner_id = int(os.getenv('OWNER_ID'))
        else:
            self.bot_app_info = await self.application_info()
            self.owner_id = self.bot_app_info.owner.id
        await self.load_cogs()

    async def load_cogs(self) -> None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                print(f'Loading extension {filename}...')
                try:
                    await self.load_extension(f'cogs.{filename[: -3]}')
                except (ExtensionFailed, ExtensionNotFound, NoEntryPointError):
                    traceback.print_exc()

    async def close(self) -> None:
        await self.session.close()
        await super().close()

    async def on_ready(self) -> None:
        await self.tree.sync()
        print(f"\nLogged in as: {self.user}\n\n BOT IS READY !")
        print(f"Version: {self.bot_version}")

        # bot presence
        cycle_status = ('^_~', "error!", '(╯°□°）╯︵ ┻━┻', "fixed", '┳━┳ ノ( ゜-゜ノ)')
        activity_type = (
            discord.ActivityType.listening, discord.ActivityType.streaming, discord.ActivityType.playing
                , discord.ActivityType.competing, discord.ActivityType.streaming)
        counter = 0
        while True:
            await asyncio.sleep(3)
            await self.change_presence(activity=discord.Activity(type=activity_type[counter], name=cycle_status[counter]))
            if counter == 4:
                counter = 0
            else:
                counter += 1

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)


def run_bot() -> None:
    bot = KtunAiLabBot()
    asyncio.run(bot.start(debug=True))


if __name__ == '__main__':
    run_bot()
