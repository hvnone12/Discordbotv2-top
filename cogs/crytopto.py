import discord
import utils.data as data
from utils.roles import get_role
from discord.ext import commands
import asyncio
import requests
import json


class CoinNotFoundException(Exception):
    pass


base_url = 'https://api.coinmarketcap.com/v1/'
global_url = 'https://api.coinmarketcap.com/v1/global/'
currencies = 'https://coinmarketcap.com/currencies/'


class Crytopto:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def coin(self, ctx, param: str=None):
        try:
            # Get the json response
            resp = requests.get(base_url + 'ticker/' + param)
            resp_json = resp.json()

            coin = resp_json[0]
            embed = get_embed_from_coin(coin)

            await ctx.send(embed=embed)

        except CoinNotFoundException:
            await ctx.send('Moneda nu a fost găsită!')


    async def on_message(self, message: discord.Message):

        if message.author.id == self.bot.user.id:
            return

        if message.content.startswith('$'):
            ticker = message.content[1:]
            coin = get_coin_from_ticker(ticker)
            try:
                embed = get_embed_from_coin(coin)
                await message.channel.send(embed=embed)
            except CoinNotFoundException:
                await message.channel.send('Moneda nu a fost găsită!')
        self.bot.process_commands(message)


def get_coin_from_ticker(ticker: str):
    resp = requests.get(base_url + 'ticker/')
    coins_json = resp.json()
    for coin_json in coins_json:
        ticker = ticker.upper()
        if ticker == coin_json['symbol']:
            return coin_json
    return {'error': 'Moneda nu a fost găsită!'}


def get_embed_from_coin(coin):
    # Check if API returns an error
    if 'error' in coin:
        raise CoinNotFoundException()

    # Retrieving values
    id = coin['id']
    name = coin['name']
    price_usd = coin['price_usd']
    price_btc = coin['price_btc']
    volume_24 = coin['24h_volume_usd']
    percent_change_1h = coin['percent_change_1h']
    percent_change_24h = coin['percent_change_24h']
    percent_change_7d = coin['percent_change_7d']
    market_cap = coin['market_cap_usd']
    rank = coin['rank']

    # Total cap requires another request
    resp = requests.get(global_url)
    resp_json = resp.json()
    total_cap = resp_json['total_market_cap_usd']

    # Creating the embed
    embed = discord.Embed(title=name, color=0xfff71e,
                          description='Rank Curent: ' + rank, url=currencies + id)
    embed.add_field(name='Valoare în USD:', value=price_usd + ' $', inline=False)
    embed.add_field(name='Valoare în BTC:', value=price_btc + ' ฿', inline=False)
    embed.add_field(name='Volum în 24h:', value=volume_24 + ' $', inline=False)
    embed.add_field(name='Market-cap:', value=market_cap + ' $', inline=False)
    embed.add_field(name='Market-cap total:', value=str(total_cap) + ' $', inline=False)
    embed.add_field(name='Modificare în 1h:', value=percent_change_1h + '%', inline=True)
    embed.add_field(name='Modificare în 24h:', value=percent_change_24h + '%', inline=True)
    embed.add_field(name='Modificare în 7z:', value=percent_change_7d + '%', inline=True)

    embed.set_thumbnail(
        url='https://mg.tools/wp-content/uploads/2017/12/1aeb569378d29bec56401dfa2d6f3852_icon.png')

    return embed


def setup(bot: commands.Bot):
    bot.add_cog(Crytopto(bot))

