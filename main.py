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
    bot_version = '0.1'
    initial_extensions = ['cogs.admin', 'cogs.events']

    # Gateway intents
    intents = discord.Intents.all()
    intents.members = True
    intents.presences = True
    intents.message_content = True

    def __init__(self):
        load_dotenv()
        super().__init__(command_prefix=self.bot_prefix, intents=self.intents)
        self.session: aiohttp.ClientSession = None
        self.owner_id = int(os.getenv('OWNER_ID'))

    # load data from .env file
    async def load_extensions(self) -> None:
        print('Loading extensions...')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f'commands.{filename[: -3]}')
                except (ExtensionFailed, ExtensionNotFound, NoEntryPointError):
                    traceback.print_exc()

    def start(self, debug: bool = False, reconnect: bool = True) -> None:
        self.debug = debug
        print(f"Bot version: {self.bot_version}")
        print(f"Bot prefix: {self.bot_prefix}")
        if self.debug:
            print("Debug mode enabled")
        await super().start(os.getenv('TOKEN'), reconnect=reconnect)
        # bot start call setup_hook

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
                try:
                    await self.load_extension(f'commands.{filename[: -3]}')
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
        activity_type = discord.ActivityType.listening
        # cycle through status
        cycle_status = cycle(['^_~', "error!", '(╯°□°）╯︵ ┻━┻', "fixed", '┳━┳ ノ( ゜-゜ノ)'])
        while True:
            await asyncio.sleep(10)
            await self.change_presence(activity=discord.Activity(type=activity_type, name=next(cycle_status)))

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Bu komut bulunamadı. Tüm mevcut komutları görmek için !help kullanın.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Gerekli argümanlar eksik: {error.param}')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'İlgili izinleriniz yok: {error.missing_perms}')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'Bu botun gerekli izinleri yok: {error.missing_perms}')
        elif isinstance(error, commands.NotOwner):
            await ctx.send('Bu botun sahibi siz değilsiniz.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('Bu komut devre dışı bırakılmış durumda.')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Bu komut soğuma sürecinde. Tekrar deneyin {error.retry_after:.2f} saniye sonra.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Bu komutu çalıştırmak için gerekli izinleresahip değilsiniz.')
        else:
            await ctx.send('Bu komut işlenirken bir hata oluştu.')
            traceback.print_exception(type(error), error, None)


def run_bot() -> None:
    bot = KtunAiLabBot()
    asyncio.run(bot.start())


if __name__ == '__main__':
    run_bot()
