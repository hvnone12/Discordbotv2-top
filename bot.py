import sys
import traceback
import discord
from discord.ext import commands
import utils.data as data
import utils.roles
import asyncio
from subhandler import SubHandler
import config

description = '''Bot'''

modules = {'cogs.roles_management', 'cogs.roles_config', 'cogs.cleaner', 'cogs.crytopto', 'cogs.greeter'}

bot = SubHandler(command_prefix='.', description=description)


@bot.event
async def on_ready():
    print('Amnesio Bot starting...')

    print(bot.user.name)
    print(bot.user.id)
    data.server = bot.get_guild(config.server_id)
    everyone = data.server.members
    online_members = list(filter(lambda x: x.status.value == 'online' , everyone))
    online_members2 = list(filter(lambda y: y.status.value == 'idle' , everyone))
    online_members3 = list(filter(lambda z: z.status.value == 'dnd' , everyone))
    online_membersfin = list(set(online_members+online_members2+online_members3))
    await bot.change_presence(game=discord.Game(name='{} din {} Online'.format(online_membersfin.__len__(), everyone.__len__())))
    print('Loading cogs...')
    if __name__ == '__main__':
        modules_loaded = 0
        for module in modules:
            try:
                bot.load_extension(module)
                print('\t' + module)
                modules_loaded += 1
            except Exception as e:
                traceback.print_exc()
                print('Error loading the extension {module}', file=sys.stderr)
        print(str(modules_loaded) + '/' + str(modules.__len__()) + ' modules loaded')
        print('Systems 100%')
        print(data.server.name)
    print('------')


@bot.event
async def on_member_join(member: discord.Member):
    if member.id in data.joined:
        print('Bang!')
        await member.send('LOL, you got banned :D :D!')
        await member.ban()
        #del data.joined[member.id]
    data.joined.append(member.id)

# Test bot
bot.run(config.bot_token)
