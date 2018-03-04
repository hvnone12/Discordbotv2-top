import utils.data as data
from discord.ext import commands
from datetime import datetime, timedelta


class CountdownCommands:
    def __init__(self, bot):
        self.bot = bot
        self.countdown = None

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def set_countdown(self, ctx, hours: int):
        """<hours> sets a countdown"""
        now = datetime.now() + timedelta(hours=hours)
        self.countdown = now
        await self.bot.say('Countdown set!')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def cancel_countdown(self):
        """Cancels current countdown"""
        self.countdown = None
        await self.bot.say('Countdown canceled!')

    @commands.command(pass_context=True)
    async def event(self):
        """Shows the current countdown"""
        if self.countdown is None:
            await self.bot.say('There is no event scheduled... ')
            return
        now = datetime.now()
        time_left = self.countdown - now
        days, seconds = time_left.days, time_left.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        await self.bot.say('```python\n {} hours {} minutes {} seconds until Grand Opening!```'.format(hours, minutes, seconds))


def setup(bot: commands.Bot):
    bot.add_cog(CountdownCommands(bot))
