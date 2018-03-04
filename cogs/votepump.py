import utils.data as data
from discord.ext import commands
from datetime import datetime, timedelta
from utils.vote_weight import get_vote_weight
import operator
import random


class VotePump:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voting = None
        self.voters = None
        self.voting_channel = None

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def start_voting(self, ctx):
        """Sets a voting"""
        self.voting = {}
        self.voters = []
        self.voting_channel = ctx.message.channel
        await self.bot.say('Coin voting started!')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def finish_voting(self):
        """Finishes current voting"""
        if self.voting is None:
            await self.bot.say('There is not a coin voting... ')
            return
        sorted_voting = sorted(self.voting.items(), key=operator.itemgetter(1), reverse=True)
        sorted_voting = sorted_voting[:5]
        print(sorted_voting)
        await self.bot.say('Countdown finished!\n These are the more voted coins:')
        for coin in sorted_voting:
            await self.bot.say('$' + coin[0])
        coin = random.choice(sorted_voting)
        await self.bot.say('```The coin is... {} ```'.format(coin[0]))
        self.voters = None
        self.voting = None
        self.voting_channel = None

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def voting_status(self):
        """Finishes current voting"""
        if self.voting is None:
            await self.bot.say('There is not a coin voting... ')
            return
        sorted_voting = sorted(self.voting.items(), key=operator.itemgetter(1), reverse=True)
        sorted_voting = sorted_voting[:5]
        print(sorted_voting)
        await self.bot.say('Top 5:')
        for coin in sorted_voting:
            await self.bot.say('$' + coin[0])

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def cancel_voting(self):
        """Cancels current voting"""
        self.voters = None
        self.voting = None
        self.voting_channel = None
        await self.bot.say('Coin voting canceled!')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def remove_coin_vote(self, ctx,  coin: str):
        """Cancels current voting"""
        if coin in self.voting:
            del self.voting[coin]

    @commands.command(name='coinname', pass_context=True)
    async def coin_name(self, ctx, coin: str):
        """Shows the current voting"""
        if self.voting is None:
            await self.bot.say('There is not a coin voting... ')
            return

        if self.voting_channel.name != ctx.message.channel.name:
            await self.bot.say('This voting is in the {} channel'.format(self.voting_channel.name))
            return

        author = ctx.message.author
        coin = coin.upper()
        if author.id in self.voters:
            self.bot.say('You have already voted!')
            return
        self.voters.append(author.id)
        if coin not in self.voting:
            self.voting[coin] = get_vote_weight(author.top_role.name)
        else:
            self.voting[coin] += get_vote_weight(author.top_role.name)
        await self.bot.say('```Vote registered!```')


def setup(bot: commands.Bot):
    bot.add_cog(VotePump(bot))
