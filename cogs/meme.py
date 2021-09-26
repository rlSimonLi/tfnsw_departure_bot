import discord
from discord.ext import commands


class Meme(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def furret(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/537428983327752242/600912641497497628/599.gif')

    @commands.command()
    async def miku(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/577084813043957773/615402893624737792/miku.gif')


def setup(client):
    client.add_cog(Meme(client))
