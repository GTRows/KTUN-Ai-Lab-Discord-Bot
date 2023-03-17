import traceback

from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
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


async def setup(client):
    await client.add_cog(Errors(client))
