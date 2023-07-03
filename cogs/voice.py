import sys

import discord
import asyncio
from discord.ext import commands
import traceback
import sqlite3
import validators

import functions


class voice(commands.Cog):

    def __init__(self, bot):
        self.database_path = bot.database_config.path
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print("Voice State Update")
        print("Member", member)

        try:
            print("connecting to DB")
            conn = sqlite3.connect(self.database_path)
            print("Connected to DB")
        except:
            print("Error connecting to DB")

        c = conn.cursor()
        guildID = member.guild.id
        print("Guild ID", guildID)
        try:
            print(f"SELECT voiceChannelID FROM guild WHERE guildID = {guildID}")
            c.execute("SELECT voiceChannelID FROM guild WHERE guildID = ?", (guildID,))
        except Exception as e:
            print("Error getting error: " + str(e))
            c.execute("SELECT voiceChannelID FROM guild")
            print(c.fetchone())
        voice = c.fetchone()
        print("Voice Channel ID", voice)
        if voice is None:
            print("Voice Channel ID is None")
            pass
        else:
            voiceID = voice[0]
            try:
                print("try")
                if after.channel.id == voiceID:
                    c.execute("SELECT * FROM voiceChannel WHERE userID = ?", (member.id,))
                    cooldown = c.fetchone()
                    if cooldown is None:
                        pass
                    else:
                        await member.send("Creating channels too quickly you've been put on a 3 second cooldown!")
                        await asyncio.sleep(3)
                    c.execute("SELECT voiceCategoryID FROM guild WHERE guildID = ?", (guildID,))
                    voice = c.fetchone()
                    c.execute("SELECT channelName, channelLimit FROM userSettings WHERE userID = ?", (member.id,))
                    setting = c.fetchone()
                    c.execute("SELECT channelLimit FROM guildSettings WHERE guildID = ?", (guildID,))
                    guildSetting = c.fetchone()
                    if setting is None:
                        name = f"{member.name}'nın odası"
                        if guildSetting is None:
                            limit = 0
                        else:
                            limit = guildSetting[0]
                    else:
                        if guildSetting is None:
                            name = setting[0]
                            limit = setting[1]
                        elif guildSetting is not None and setting[1] == 0:
                            name = setting[0]
                            limit = guildSetting[0]
                        else:
                            name = setting[0]
                            limit = setting[1]
                    categoryID = voice[0]
                    id = member.id
                    category = self.bot.get_channel(categoryID)
                    channel2 = await member.guild.create_voice_channel(name, category=category)
                    channelID = channel2.id
                    await member.move_to(channel2)
                    await channel2.set_permissions(self.bot.user, connect=True, read_messages=True)
                    await channel2.edit(name=name, user_limit=limit)
                    c.execute("INSERT INTO voiceChannel VALUES (?, ?)", (id, channelID))
                    conn.commit()

                    def check(a, b, c):
                        return len(channel2.members) == 0

                    await self.bot.wait_for('voice_state_update', check=check)
                    await channel2.delete()
                    await asyncio.sleep(3)
                    c.execute('DELETE FROM voiceChannel WHERE userID=?', (id,))
            except:
                print("Error")
                print("after.channel")
                print(sys.exc_info())
                pass
        conn.commit()
        conn.close()

    @commands.command()
    @commands.check(functions.is_it_me)
    async def voice_help(self, ctx, channel=None):
        embed = discord.Embed(title="Komutlar", description="", color=0x7289da)
        embed.set_author(name=f"{ctx.guild.me.display_name}", url="",
                         icon_url=f"{ctx.guild.me.display_avatar.url}")
        embed.add_field(name=f'**Voice Commands**',
                        value=f'**Odayı kilitler. İzin vermediğiniz kişiler kanalınıza giremez:**\n\n`!voice lock`\n\n------------\n\n'
                              f'**Odanın kilidini açar:**\n\n`!voice unlock`\n\n------------\n\n'
                              f'**Odanın adını değiştirmenizi sağlar:**\n\n`!voice name <name>`\n\n------------\n\n'
                              f'**Odanın kişi limitini belirler:**\n\n`!voice limit <number>`\n\n------------\n\n'
                              f'**Odanızı kilitlediğinizde odanıza birinin girebilmesi için yetki verir:**\n\n`!voice permit @person`\n\n------------\n\n'
                              f'**Odaya girmesini istemediğiniz kişiler için komuttur:**\n\n`!voice reject @person`\n\n------------\n\n'
                              f'**Odanın asıl sahibi çıkarsa, odanın yetkilerini devralmanızı sağlayan komut:**\n\n`!voice claim`',
                        inline='false')
        if channel is not None:
            if channel[0] == '<' and channel[-1] == '>':
                channel = channel[2:-1]
            try:
                channel = int(channel)
            except ValueError:
                await ctx.send("ValueError <@317674611628179456>")
            ch = self.bot.get_channel(channel)
            await ch.send(embed=embed)
        else:
            await ctx.channel.send(embed=embed)

    @commands.group()
    async def voice(self, ctx):
        pass

    @voice.command()
    async def setup(self, ctx):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        guildID = ctx.guild.id
        id = ctx.author.id
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 317674611628179456:
            def check(m):
                return m.author.id == ctx.author.id

            await ctx.channel.send("**You have 60 seconds to answer each question!**")
            await ctx.channel.send(
                f"**Enter the name of the category you wish to create the channels in:(e.g Voice Channels)**")
            try:
                category = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.channel.send('Took too long to answer!')
            else:
                new_cat = await ctx.guild.create_category_channel(category.content)
                await ctx.channel.send('**Enter the name of the voice channel: (e.g Join To Create)**')
                try:
                    channel = await self.bot.wait_for('message', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    await ctx.channel.send('Took too long to answer!')
                else:
                    try:
                        print("Creating channel", channel.content, "in category", new_cat.name)
                        channel = await ctx.guild.create_voice_channel(channel.content, category=new_cat)
                        print("Channel created")
                        c.execute("SELECT * FROM guild WHERE guildID = ? AND ownerID=?", (guildID, id))
                        print("Checking if guild is in database")
                        voice = c.fetchone()
                        print("Checking if owner is in database")
                        if voice is None:
                            print("Adding guild to database")
                            c.execute("INSERT INTO guild VALUES (?, ?, ?, ?)", (guildID, id, channel.id, new_cat.id))
                        else:
                            print("Updating guild in database")
                            c.execute(
                                "UPDATE guild SET guildID = ?, ownerID = ?, voiceChannelID = ?, voiceCategoryID = ? WHERE guildID = ?",
                                (guildID, id, channel.id, new_cat.id, guildID))
                            print("Guild updated")
                        await ctx.channel.send("**You are all setup and ready to go!**")
                        print("Setup complete")
                    except:
                        print("Error creating channel")
                        print("error:", sys.exc_info()[0])
                        await ctx.channel.send("You didn't enter the names properly.\nUse `!voice setup` again!")
        else:
            await ctx.channel.send(f"{ctx.author.mention} bu komudu sadece server sahibi kullanabilir!")
        conn.commit()
        conn.close()

    @commands.command()
    async def setlimit(self, ctx, num):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        if ctx.author.id == ctx.guild.owner.id or ctx.author.id == 151028268856770560:
            c.execute("SELECT * FROM guildSettings WHERE guildID = ?", (ctx.guild.id,))
            voice = c.fetchone()
            if voice is None:
                c.execute("INSERT INTO guildSettings VALUES (?, ?, ?)",
                          (ctx.guild.id, f"{ctx.author.name}'s channel", num))
            else:
                c.execute("UPDATE guildSettings SET channelLimit = ? WHERE guildID = ?", (num, ctx.guild.id))
            await ctx.send("You have changed the default channel limit for your server!")
        else:
            await ctx.channel.send(f"{ctx.author.mention} only the owner of the server can setup the bot!")
        conn.commit()
        conn.close()

    @setup.error
    async def info_error(self, ctx, error):
        print(error)

    @voice.command()
    async def lock(self, ctx):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice = c.fetchone()
        if voice is None:
            await ctx.channel.send(f"{ctx.author.mention} You don't own a channel.")
        else:
            channelID = voice[0]
            role = ctx.guild.default_role
            channel = self.bot.get_channel(channelID)
            await channel.set_permissions(role, connect=False)
            await ctx.channel.send(f'{ctx.author.mention} Voice chat locked! 🔒')
        conn.commit()
        conn.close()

    @voice.command()
    async def unlock(self, ctx):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice = c.fetchone()
        if voice is None:
            await ctx.channel.send(f"{ctx.author.mention} You don't own a channel.")
        else:
            channelID = voice[0]
            role = ctx.guild.default_role
            channel = self.bot.get_channel(channelID)
            await channel.set_permissions(role, connect=True)
            await ctx.channel.send(f'{ctx.author.mention} Voice chat unlocked! 🔓')
        conn.commit()
        conn.close()

    @voice.command(aliases=["allow"])
    async def permit(self, ctx, member: discord.Member):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice = c.fetchone()
        if voice is None:
            await ctx.channel.send(f"{ctx.author.mention} You don't own a channel.")
        else:
            channelID = voice[0]
            channel = self.bot.get_channel(channelID)
            await channel.set_permissions(member, connect=True)
            await ctx.channel.send(
                f'{ctx.author.mention} You have permited {member.name} to have access to the channel. ✅')
        conn.commit()
        conn.close()

    @voice.command(aliases=["deny"])
    async def reject(self, ctx, member: discord.Member):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        id = ctx.author.id
        guildID = ctx.guild.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice = c.fetchone()
        if voice is None:
            await ctx.channel.send(f"{ctx.author.mention} You don't own a channel.")
        else:
            channelID = voice[0]
            channel = self.bot.get_channel(channelID)
            for members in channel.members:
                if members.id == member.id:
                    c.execute("SELECT voiceChannelID FROM guild WHERE guildID = ?", (guildID,))
                    voice = c.fetchone()
                    channel2 = self.bot.get_channel(voice[0])
                    await member.move_to(channel2)
            await channel.set_permissions(member, connect=False, read_messages=True)
            await ctx.channel.send(
                f'{ctx.author.mention} You have rejected {member.name} from accessing the channel. ❌')
        conn.commit()
        conn.close()

    @voice.command()
    async def limit(self, ctx, limit):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice = c.fetchone()
        if voice is None:
            await ctx.channel.send(f"{ctx.author.mention} You don't own a channel.")
        else:
            channelID = voice[0]
            channel = self.bot.get_channel(channelID)
            await channel.edit(user_limit=limit)
            await ctx.channel.send(f'{ctx.author.mention} You have set the channel limit to be ' + '{}!'.format(limit))
            c.execute("SELECT channelName FROM userSettings WHERE userID = ?", (id,))
            voice = c.fetchone()
            if voice is None:
                c.execute("INSERT INTO userSettings VALUES (?, ?, ?)", (id, f'{ctx.author.name}', limit))
            else:
                c.execute("UPDATE userSettings SET channelLimit = ? WHERE userID = ?", (limit, id))
        conn.commit()
        conn.close()

    @voice.command()
    async def name(self, ctx, *, name):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice = c.fetchone()
        if voice is None:
            await ctx.channel.send(f"{ctx.author.mention} You don't own a channel.")
        else:
            channelID = voice[0]
            channel = self.bot.get_channel(channelID)
            await channel.edit(name=name)
            await ctx.channel.send(f'{ctx.author.mention} You have changed the channel name to ' + '{}!'.format(name))
            c.execute("SELECT channelName FROM userSettings WHERE userID = ?", (id,))
            voice = c.fetchone()
            if voice is None:
                c.execute("INSERT INTO userSettings VALUES (?, ?, ?)", (id, name, 0))
            else:
                c.execute("UPDATE userSettings SET channelName = ? WHERE userID = ?", (name, id))
        conn.commit()
        conn.close()

    @voice.command()
    async def claim(self, ctx):
        x = False
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        channel = ctx.author.voice.channel
        if channel == None:
            await ctx.channel.send(f"{ctx.author.mention} you're not in a voice channel.")
        else:
            id = ctx.author.id
            c.execute("SELECT userID FROM voiceChannel WHERE voiceID = ?", (channel.id,))
            voice = c.fetchone()
            if voice is None:
                await ctx.channel.send(f"{ctx.author.mention} You can't own that channel!")
            else:
                for data in channel.members:
                    if data.id == voice[0]:
                        owner = ctx.guild.get_member(voice[0])
                        await ctx.channel.send(
                            f"{ctx.author.mention} This channel is already owned by {owner.mention}!")
                        x = True
                if x == False:
                    await ctx.channel.send(f"{ctx.author.mention} You are now the owner of the channel!")
                    c.execute("UPDATE voiceChannel SET userID = ? WHERE voiceID = ?", (id, channel.id))
            conn.commit()
            conn.close()


async def setup(bot):
    await bot.add_cog(voice(bot))
