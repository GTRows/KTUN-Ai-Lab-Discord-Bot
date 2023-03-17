import time
import discord
from discord.ext import commands
import functions


class UserCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(functions.is_it_me)
    async def search(self, ctx, *, content):
        """
        Let me google that
        """
        await ctx.channel.send("Google'da arıyorum lütfen bekleyin. :mechanic:")
        await ctx.channel.send("https://letmegooglethat.com/?q=" + content.replace(" ", "_"))

    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """ İstediğiniz kişinin ppsini embed şeklinde atar. """
        user = user or ctx.author

        avatars_list = []

        def target_avatar_formats(target):
            formats = ["JPEG", "PNG", "WebP"]
            if target.is_animated():
                formats.append("GIF")
            return formats

        if not user.avatar and not user.guild_avatar:
            return await ctx.send(f"**{user}** has no avatar set, at all...")

        if user.avatar:
            avatars_list.append("**Account avatar:** " + " **-** ".join(
                f"[{img_format}]({user.avatar.replace(format=img_format.lower(), size=1024)})"
                for img_format in target_avatar_formats(user.avatar)
            ))

        embed = discord.Embed(colour=user.top_role.colour.value)

        if user.guild_avatar:
            avatars_list.append("**Server avatar:** " + " **-** ".join(
                f"[{img_format}]({user.guild_avatar.replace(format=img_format.lower(), size=1024)})"
                for img_format in target_avatar_formats(user.guild_avatar)
            ))
            embed.set_thumbnail(url=user.avatar.replace(format="png"))

        embed.set_image(url=f"{user.display_avatar.with_size(256).with_static_format('png')}")
        embed.description = "\n".join(avatars_list)

        await ctx.send(f"🖼 Avatar to **{user}**", embed=embed)

    @commands.command()
    async def ping(self, ctx) -> None:
        """
        Botun aktif olup olmadığını kontrol eder.

        :param context: The hybrid command context.
        """
        before = time.monotonic()
        before_ws = int(round(self.client.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is WS: {before_ws}ms  |  REST: {int(ping)}ms.",
            color=0x9C84EF,
        )
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(UserCog(client))
