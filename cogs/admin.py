import discord
from discord.ext import commands
from discord import app_commands
import functions


class AdminCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    @app_commands.command()
    @app_commands.choices(choices=[
            app_commands.Choice(name="Rock", value="rock"),
            app_commands.Choice(name="Paper", value="paper"),
            app_commands.Choice(name="Scissors", value="scissors"),
        ])
    async def test(self, i: discord.Interaction, choices: app_commands.Choice[str]):
        """
        Test bot's latency
        :param ctx:
        :return:
        """
        print("test function called")
        print(i)
        await i.response.send_message(f'Pong! ', choices)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def send_embed(self, ctx, channel = "<#1074063844411981955>"):
        """
        admin commands
        """
        ch = functions.get_channel_by_id(self.client, channel)
        embed = discord.Embed(title="Mezun Söyleyişi - Zeki Dişçi - Java ve Java Teknolojileri")
        embed.set_author(name="KTUN AI Lab",
                         icon_url="https://media.discordapp.net/attachments/1086371529564094554/1086372841273950268/Varlk_898x.png?width=676&height=676")
        embed.set_image(url="https://media.discordapp.net/attachments/1086371529564094554/1086371592981987439/Soyleyisi1.jpg?width=676&height=676")
        embed.add_field(name="",
                        value="""
                        Okulumuzun değerli bilgisayar mühendisliği mezunları ile sizleri buluşturmak adına planladığımız serinin ilk webinarı 22 Mart saat 20.00'de discord sunucumuzda sizleri bekliyor! ⏰⏰

2019 yılında KTÜN Bilgisayar Mühendisliği bölümünden mezun olmuş olan ve şu anda Bilgi Teknolojileri ve İletişim Kurumu'nda Java Software Developer olarak çalışan Zeki Dişçi ile sizleri buluşturacağız. 
Etkinlikte öğrencilik yılları ve deneyimleriyle birlikte yazılım dünyasında önemli bir yeri olan Java programla dili, Java kullanarak yazılım sistemlerinin geliştirilmesi ve üretim süreçleri ile ilgili bilgiler alabileceğiniz gibi aklınıza takılan soruları da sorabileceksiniz.
Etkinlik Discord üzerinden gerçekleştirilecektir.""",
                        inline=True)
        embed.set_footer(text="KTUN Bilişim Topluluğu")
        embed.set_image(url="https://media.discordapp.net/attachments/1086371529564094554/1086371592981987439/Soyleyisi1.jpg")
        await ch.send(embed=embed)

    @commands.command()
    @commands.check(functions.is_it_me)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        admin commands
        """
        await member.kick(reason=reason)
        await ctx.send("kicked")

    @commands.command()
    @commands.check(functions.is_it_me)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """
        admin commands
        """
        await member.ban(reason=reason)
        await ctx.send("banned")

    @commands.command()
    @commands.check(functions.is_it_me)
    async def clear(self, ctx, amount):
        """
        admin commands
        """
        try:
            amount = int(amount)
        except:
            if amount == "all":
                amount = 100
            else:
                await ctx.send("tam sayı bir değer giriniz.")
                return
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            description=f"**{ctx.author}** cleared **{amount}** messages!",
            color=0x9C84EF,
        )
        await ctx.channel.send(embed=embed)
        # clear all eklenecek

    @commands.command()
    @commands.check(functions.is_it_me)
    async def logout(self, ctx):
        """
        admin commands
        """
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0x9C84EF)
        await ctx.send(embed=embed)
        await self.client.close()

    @commands.command()
    @commands.check(functions.is_it_me)
    async def message_it(self, ctx, member: discord.User, *, content):
        """
        admin commands
        """
        await member.send(content)

    @commands.command()
    @commands.check(functions.is_it_me)
    async def message_channel(self, ctx, channel, *, content):
        """
        admin commands
        """
        if channel[0] == '<' and channel[-1] == '>':
            channel = channel[2:-1]
        try:
            channel = int(channel)
        except ValueError:
            await ctx.send("ValueError <@317674611628179456>")
        ch = self.client.get_channel(channel)
        await ch.send(content)

    @commands.command()
    @commands.check(functions.is_it_me)
    async def serverinfo(self, ctx) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in ctx.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{ctx.guild}", color=0x9C84EF
        )
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name="Server ID", value=ctx.guild.id)
        embed.add_field(name="Member Count", value=ctx.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(ctx.guild.channels)}"
        )
        embed.add_field(name=f"Roles ({len(ctx.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {ctx.guild.created_at}")
        await ctx.send(embed=embed)

    @commands.command(name='restart')
    @commands.check(functions.is_it_me)
    async def restart(self, ctx):
        """
        admin commands
        """
        await ctx.send("Restarting bot...")
        functions.restart_client()


async def setup(client):
    await client.add_cog(AdminCog(client))
