import discord
import utils.data as data
from utils.roles import get_role, get_next_role, roles
from discord.ext import commands
import asyncio


class Secret:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def createchannel(self, ctx, channel_name):
        """<channel-name> Invite channel"""
        server = ctx.message.server

        # Setup initial permissions
        permissions = discord.PermissionOverwrite(read_messages=False)
        mine = discord.PermissionOverwrite(read_messages=True)
        # Create secret channel
        channel = await self.bot.create_channel(ctx.message.server, channel_name,
                                                (server.default_role, permissions), (server.me, mine))
        initial_message = await self.bot.send_message(channel,
                                                      '**{}** created. Now I\'ll invite users ordered by rank...'
                                                      .format(channel_name))

        invites_keys = roles.keys()
        invites_keys = sorted(invites_keys, reverse=True)
        for invites_needed in invites_keys:
            rank = roles[invites_needed]
            role = discord.utils.get(server.roles, name=rank)
            rank_message = await self.bot.send_message(channel, '{} now!'.format(role.mention))

            await self.bot.edit_channel_permissions(channel, role, mine)
            await asyncio.sleep(5)
            if rank_message is not None:
                await self.bot.delete_message(rank_message)
        # Final clean up
        await self.bot.edit_channel_permissions(channel, server.default_role, mine)
        await self.bot.edit_message(initial_message, 'Finished!')


def setup(bot: commands.Bot):
    bot.add_cog(Secret(bot))
