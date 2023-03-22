import json
import discord
from random import randint
from discord.ext import commands
from functions import is_it_me


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(is_it_me)
    @commands.has_permissions(administrator=True)
    async def createticket(self, ctx, *args):
        format_args = list(args)

        try:
            guild_id = ctx.message.guild.id
            channel_id = int(format_args[0].strip('<').strip('>').replace('#', ''))
            title = ' '.join(format_args[1:])
        except ValueError:
            await ctx.send('ValueError')
            return
        except IndexError:
            await ctx.send('IndexError')
            return


        with open('.\\databases\\ticket.json', 'r+') as file:
            ticket_data = json.load(file)
            new_ticket = str(guild_id)

            # Update existing ticket
            if new_ticket in ticket_data:

                ticket_data[new_ticket] += [channel_id]
                with open('.\\databases\\ticket.json', 'w') as update_ticket_data:
                    json.dump(ticket_data, update_ticket_data, indent=4)

            # Add new ticket
            else:
                ticket_data[new_ticket] = [channel_id]
                with open('.\\databases\\ticket.json', 'w') as new_ticket_data:
                    json.dump(ticket_data, new_ticket_data, indent=4)

        # Create new embed with reaction
        ticket_embed = discord.Embed(colour=randint(0, 0xffffff))
        ticket_embed.set_thumbnail(
            url=f'https://cdn.discordapp.com/icons/{guild_id}/{ctx.message.guild.icon}.png')

        ticket_embed.add_field(name=f'{ctx.message.guild} Serverına hoş geldiniz.', value=f'{title}')
        send_ticket_embed = await self.client.get_channel(channel_id).send(embed=ticket_embed)

        await send_ticket_embed.add_reaction(u'\U0001F3AB')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def closeticket(self, ctx, mentioed_user):
        await ctx.message.channel.delete(reason=None)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.client.user.id:
            with open('.\\databases\\ticket.json', 'r') as file:
                ticket_data = json.load(file)

            channel_id = list(ticket_data.values())
            user_channel_id = payload.channel_id

            for items in channel_id:
                if user_channel_id in items:
                    role = discord.utils.find(lambda r: r.name == 'member', payload.member.guild.roles)
                    if role in payload.member.roles:
                        user = self.client.get_user(int(payload.member.id))
                        await user.send("You are already member")
                        continue
                    # Get guild and roles
                    find_guild = discord.utils.find(lambda guild: guild.id == payload.guild_id, self.client.guilds)

                    # Create new role
                    permissions = discord.Permissions(send_messages=True, read_messages=True)
                    await find_guild.create_role(name=f'{payload.member.name}', permissions=permissions)

                    # Assign new role
                    new_user_role = discord.utils.get(find_guild.roles, name=f'{payload.member.name}')
                    await payload.member.add_roles(new_user_role, reason=None, atomic=True)

                    overwrites = {
                        find_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        payload.member: discord.PermissionOverwrite(read_messages=True),
                    }

                    # Create new channel
                    create_channel = await find_guild.create_text_channel(
                        u'\U0001F4CB-{}'.format(payload.member), overwrites=overwrites)

                    await create_channel.send(
                        'Başvurunuzu aldık lütfen İsminizi Soyisminizi Okul mail adresinizi yazınız ve onaylanmasını bekleyiniz. Onaylandığınızda oda otamatik olarak silinecek ve isminiz değiştirilecektir. Herhangi bir sorunuz varsa yazabilirsiniz.')


async def setup(client):
    pass
    # await client.add_cog(Ticket(client))
