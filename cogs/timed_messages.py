from discord.ext import commands
import discord
import asyncio
import utils.data as data


class MessagesTimer:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.roles = {}
        self.timer = 0
        self.bot.loop.create_task(self.messages_timer())

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def add_timed_role(self, ctx, role: discord.Role):
        if role.id not in self.roles:
            self.roles[role.id] = role
            await self.bot.say('Role added to timed messages')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def remove_timed_role(self, ctx, role: discord.Role):
        if role.id not in self.roles:
            self.roles[role.id] = role
            await self.bot.say('Role added to timed messages')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def set_timer(self, ctx, user_timer: float):
        self.timer = user_timer

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def cancel_timer(self, ctx):
        self.timer = 0

    async def messages_timer(self):
        while not self.bot.is_closed:
            if self.timer == 0:
                await asyncio.sleep(5)
                continue
            await asyncio.sleep(60 * self.timer)
            members = data.server.members
            for role in self.roles.values():
                print('Now messaging {}'.format(role))
                role_members = list(filter(lambda x: role in x.roles, members))
                print(role_members)
                for role_member in role_members:
                    await self.bot.send_message(role_member, 'Sample message')


def setup(bot: commands.Bot):
    bot.add_cog(MessagesTimer(bot))

