import discord
from discord.ext import commands

import functions


class AdminCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def send_embed(self, ctx, channel):
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
        embed = discord.Embed(title="Başvuru Formu", url="https://forms.gle/ZQQA128LuP9tm4hY9")
        embed.set_author(name="KTUN AI Lab", url="https://gtrows.com",
                         icon_url="https://cdn.discordapp.com/avatars/875055421675667496/c02bbd09488e9c8ffbbcb1b1e588b62d.webp?size=80")
        # embed.set_thumbnail(
        #     url="https://www.teknofest.org/upload/31b959abfaec671eaef701d914965f01.png")
        # https://cdn.discordapp.com/avatars/336548700803301380/f6109faa5d139b07b81a5bce850fea7e.webp?size=128
        embed.add_field(name="E-Ticaret Yapay Zeka Takımı",
                        value="Başvurularınızı bekliyoruz.",
                        inline=False)
        embed.set_footer(text="Takım kaptanı: Mehmet Demircan")
        # embed.set_image(
        #    url="https://instagram.fist13-1.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/s640x640/246535393_287308349908957_8488703921768336750_n.webp.jpg?_nc_ht=instagram.fist13-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=ZHx_MrEJDJEAX_IJ75V&tn=vFjocogaCOzh3Azd&edm=AP_V10EBAAAA&ccb=7-4&oh=746b2c703a29c1a65ae26f00d0f46789&oe=61763677&_nc_sid=4f375e")
        await ch.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test(self, ctx, *, content):
        print(content)

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
