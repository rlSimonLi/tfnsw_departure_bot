import discord
import os
from discord.ext import commands, tasks
from lib.tfnsw import Transit
from itertools import cycle


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.current_departures = []
        self.departure_index = cycle([0, 1, 2, 3])

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_departures.start()
        self.update_status.start()
        print("Student Centre is now opened :)")

    @tasks.loop(seconds=15)
    async def update_status(self):
        departure = self.current_departures[next(self.departure_index)]
        await self.client.change_presence(activity=discord.Game(departure.get_short_desc()))

    @tasks.loop(seconds=60)
    async def update_departures(self):
        self.current_departures = Transit.fetch_departures(10101421, 'train')[1]

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Bruh! The latency is {}ms.'.format(round(self.client.latency * 1000)))

    @commands.command()
    async def version(self, ctx):
        if os.environ['BOT_MODE'] == 'production':
            await ctx.send("Production: Version 01.03.2020")
        elif os.environ['BOT_MODE'] == 'development':
            await ctx.send("Experimental: Version 01.03.2020")


def setup(client):
    client.add_cog(Basic(client))
