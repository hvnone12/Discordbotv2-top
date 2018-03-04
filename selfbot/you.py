import discord
from discord.ext import commands
import asyncio
import datetime
import self_config
import asyncpg

bot = commands.Bot(command_prefix=".")
bot.active=False
@bot.event
async def on_ready():
    c = await asyncpg.connect(self_config.postgres_uri)
    await c.execute('''DROP TABLE entries''')
    await c.execute('''CREATE TABLE if not exists entries(
        id serial PRIMARY KEY,
        message text,
        channel_id bigint
    )''')
    await c.close()
    print("Spy-mode ready")
    print("Username:", bot.user.name)
    print("User ID:", bot.user.id)
@bot.event
async def on_message(message):
    if bot.active:
        if message.author!=bot.user:
            for i, server in enumerate(self_config.target_servers):
                if message.guild.id==server:
                    if message.channel.id==self_config.target_channels[i]:
                        c = await asyncpg.connect(self_config.postgres_uri)
                        content=message.content
                        if message.embeds:
                            content=message.embeds[0].description
                        await c.execute('INSERT INTO entries (message, channel_id) VALUES ($1, $2)', content, self_config.destination_channels[i])
                        await c.close()
    if message.content.startswith('spystart') and bot.active==False:
        if message.author.id==275437494751723521 or message.author.id==208948504742068226:
            bot.active=True
    if message.content.startswith('spystop') and bot.active==True:
        if message.author.id==275437494751723521 or message.author.id==208948504742068226:
            bot.active=False
    if message.content.startswith("spystatus"):
        print(bot.active)

                


bot.run(self_config.self_token, bot=False)