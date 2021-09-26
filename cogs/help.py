import discord
from discord.ext import commands

manpage = {
    'ping': '**ping**\n\nObtain the latency of the bot\nUsage: `ping`',
    'redfern': '**redfern**\n\nObtain the next 10 departures from Redfern Station\nUsage: `redfern`',
    'cityroad': '**cityroad**\n\nObtain the next 10 departures from USYD City Road bus stops\nUsage: `cityroad '
                '<north|sorth>`',
    'departure': '**departure**\n\nObtain the next 10 departures from the stop specified\nUsage: `departure '
                 '<stop_id> [bus|train|ferry|light_rail]`\n\nStop ID can be found here: '
                 'https://transportnsw.info/stops#/ > Copy the URL '
}


class Help(commands.Cog):
    ERROR_MSG = 'Please use `!help <command>` for more information.'

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, cmd):
        await ctx.send(manpage[cmd])


def setup(client):
    client.add_cog(Help(client))
