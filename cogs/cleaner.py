from discord.ext import commands
import asyncio


class Cleaner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def clean(self, ctx, lines: int=80000):
        """<number of line> (everything if no number)"""
        # Removes the lines
        async for message in ctx.message.channel.history(limit=lines):
            await message.delete()
        # Auto-remove message
        temp_message = await ctx.send('Curățat!')
        await asyncio.sleep(5)
        await temp_message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Cleaner(bot))
