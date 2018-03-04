import discord
from discord.ext import commands
import sys, traceback
import asyncio
import aiohttp
import async_timeout
import datetime
import json
from utils.manage_subscription import Subscriptions
from utils.process_data import RoleManager
import config
import selfbot.self_config
from woocommerce import API
import asyncpg

class SubHandler(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wcapi = API(
            url="https://crypto-trading.ro/",
            consumer_key="ck_74123c18aa6a5a09b14f231733de3232fea72fe6",
            consumer_secret="cs_8d2d9603060ff8969ee159d2779211772e149f58",
            wp_api=True,
            version="wc/v1"
        )
        self.manage_roles=RoleManager()
        self.session = aiohttp.ClientSession(loop=self.loop)
        bg_task=self.loop.create_task(self.handle_subscriptions())
        spy_task=self.loop.create_task(self.spy_channels())
    async def spy_channels(self):
        await self.wait_until_ready()
        
        update_role=discord.utils.get(self.get_guild(config.server_id).roles, id=config.update_role_id)
        print("Connecting to database...")
        c = await asyncpg.connect(selfbot.self_config.postgres_uri)
        print("Database connected successfully")
        while True:
            messages = await c.fetch("SELECT * FROM entries")
            for message in messages:
                try:
                    channel=self.get_channel(message['channel_id'])
                    await channel.send(update_role.mention+"\n"+message['message'])
                except Exception as e:
                    print(e)
                await c.execute("DELETE FROM entries WHERE id=$1", message['id'])
            await asyncio.sleep(1, loop=self.loop)

    async def handle_subscriptions(self):
        await self.wait_until_ready()
        while True:
            channel=self.get_channel(config.output_channel_id)
            await channel.send("Requesting subscriptions...")
            page=0
            while True:
                page+=1
                try:
                    r = self.wcapi.get('subscriptions?page={}'.format(page))
                except requests.exceptions.RequestException as e:
                    print(e)
                    print("Time out error, tries again next iteration")
                else:
                    if not r.json():
                        break
                    subscrip = Subscriptions(r.json())
                    
                    subscriptions = subscrip.sort_entries()
                    output_string=""
                    for sub in subscriptions:
                        assign_roles_id=[config.premium_role_id]
                        add_into_string="ID: {}, status: {}, type: {}, expire: {}".format(sub['discord_id'], sub['status'], sub['variation_type'], sub['days_before_expire'])
                        output_string+=f"\n**--------------**\n``{add_into_string}``\n"
                        # Checks if the subscription is active
                        assign_roles_id.append(int(sub['role_id']))
                        user=self.get_guild(config.server_id).get_member(int(sub['discord_id']))
                        # If user bound to the id exists on the server
                        if user:
                            if sub['status']=='active':
                                check = await self.manage_roles.get_cached_user(user, sub['status'])
                                if check:
                                    output_string+="Sends DM that welcomes a new user\n"
                                    await user.send(config.welcome_message)
                                else:
                                    output_string+="Does not send DM to welcome, as it's already done\n"
                                output_string+=f"{user}'s' subscription is active, assigning roles if not already done\n"
                                await self.manage_roles.role_assignment(user, assign_roles_id)
                                if sub['days_before_expire']<=1:
                                    output_string+="Sends DM that subscription is about to expire"

                                    # Sends dm
                                    await user.send(config.one_day_message)
                                    
                            if sub['status']=='expired' or sub['status']=='cancelled':
                                output_string+=f"{user.name}'s subscription have expired\n"
                                check = await self.manage_roles.get_cached_user(user, sub['status'])
                                if check:
                                    output_string+="Removing roles and sending DM"
                                    await self.manage_roles.role_removal(user, assign_roles_id)

                                    # Sends dm
                                    await user.send(config.expire_message)

                                else:
                                    output_string+="Do not send DM nor remove roles, already done"
                        else:
                            output_string+="This discord ID does not match any member on this server"
                    try:
                        embed = discord.Embed(title=f"Requests acquired from page {page}", description=output_string)
                        await channel.send(embed=embed)
                    except Exception as e:
                        print(e)

            await asyncio.sleep(60, loop=self.loop)

    async def close(self):
        print("closing")
        await super().close()
        await self.session.close()