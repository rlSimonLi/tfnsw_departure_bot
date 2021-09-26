from discord.ext import commands
from lib.tfnsw import Transit
from cogs.help import Help


class Transport(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def redfern(self, ctx):
        stop_name, departures = Transit.fetch_departures(10101421, 'train')
        response = "**__Departures: {}__**\n\n".format(stop_name)
        for departure in departures[:10]:
            response += departure.__str__() + '\n'

        await ctx.send(response)

    @commands.command()
    async def cityroad(self, ctx, stand):
        stop_id = 0
        if stand not in ('s', 'n', 'south', 'north'):
            raise AttributeError
        if stand in ('s', 'south'):
            stop_id = 10111110
        elif stand in ('n', 'north'):
            stop_id = 10113063
        stop_name, departures = Transit.fetch_departures(stop_id, 'bus')
        response = "**__Departures: {}__**\n\n".format(stop_name)
        for departure in departures[:10]:
            response += departure.__str__() + '\n'

        await ctx.send(response)

    @cityroad.error
    async def cityroad_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, AttributeError):
            await ctx.send("Please specify which stand you want." + Help.ERROR_MSG)

    @commands.command()
    async def departure(self, ctx, stop_id, mode=''):
        stop_name, departures = Transit.fetch_departures(stop_id, mode)
        response = "**__Departures: {}__**\n\n".format(stop_name)
        if len(departures) == 0:
            response += "There are no departures from this stop."
        else:
            for departure in departures[:10]:
                response += departure.__str__() + '\n'

        await ctx.send(response)

    @departure.error
    async def departure_error(self, ctx, error):
        if isinstance(error, IndexError):
            await ctx.send("Cannot find any stop with this ID." + Help.ERROR_MSG)


def setup(client):
    client.add_cog(Transport(client))
