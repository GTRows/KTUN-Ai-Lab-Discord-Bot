import discord
import asyncio
import sqlite3
import os
import sys
import traceback
import logging
import aiohttp
from discord.ext import commands, tasks
from itertools import cycle
from discord.ext.commands import ExtensionFailed, ExtensionNotFound, NoEntryPointError
from dotenv import load_dotenv
from discord import app_commands

from config_manager import ConfigManager


class KtunAiLabBot(commands.Bot):
    bot_app_info: discord.AppInfo

    def __init__(self, config_json_path: str = "config.json"):
        self.config_manager = ConfigManager(config_json_path)
        self.bot_prefix = self.config_manager.bot_config.prefix
        self.bot_version = self.config_manager.bot_config.version
        self.database_config = self.config_manager.database_config
        self.statues = cycle(self.config_manager.bot_config.activity)
        intents = discord.Intents.all()
        intents.members = self.config_manager.intents_config.members
        intents.presences = self.config_manager.intents_config.presences
        intents.message_content = self.config_manager.intents_config.message_content
        self.debug = self.config_manager.is_debug_mode()
        self.control_db()
        super().__init__(command_prefix=self.bot_prefix, intents=intents)

    def control_db(self):
        db_path = self.database_config.path
        if not os.path.exists(db_path):
            print("Database not found. Creating database...")
            conn = sqlite3.connect(db_path)

            c = conn.cursor()

            c.execute('''create table voiceChannel(userIDx INTEGER,
                        voiceID INTEGER)''')

            c.execute('''create table userSettings(userID INTEGER,
                        channelName  TEXT,
                        channelLimit INTEGER)''')

            c.execute('''create table guildSettings
                        (guildID INTEGER,
                            channelName  TEXT,
                            channelLimit INTEGER)''')

            c.execute('''create table guild(guildID INTEGER,
                        ownerID INTEGER,
                        voiceChannelID  INTEGER,
                        voiceCategoryID INTEGER)''')

            conn.commit()
            conn.close()

    async def start(self, **kwargs) -> None:
        if self.debug:
            print("Debug mode enabled")
            await super().start(self.config_manager.bot_config.test_token, reconnect=False)
        else:
            await super().start(self.config_manager.bot_config.token, reconnect=True)
        await self.tree.copy_global_to()
        await self.tree.sync()

    async def setup_hook(self) -> None:
        self.bot_app_info = await self.application_info()
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
        await self.logout()
        await self.session.close()
        await super().close()

    async def restart(self) -> None:
        await self.close()
        os.execv(sys.executable, ['python'] + sys.argv)

    async def on_ready(self) -> None:
        await self.tree.sync()
        print(f"\nLogged in as: {self.user}\n\n BOT IS READY !")
        print(f"Version: {self.bot_version}")

        self.change_status.start()

    @tasks.loop(seconds=60)  # Change status every minute
    async def change_status(self):
        await self.change_presence(activity=discord.Game(next(self.statuses)))

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)


def run_bot(config_json_path="config.json") -> None:
    bot = KtunAiLabBot(config_json_path=config_json_path)
    asyncio.run(bot.start())

if __name__ == '__main__':
    run_bot()
