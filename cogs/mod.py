import discord
from discord.ext import commands


class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def vibecheck(self, ctx, *users: discord.Member):
        guild = discord.utils.get(self.client.guilds, name='UNSW Discussion')
        for user in users:
            vibechecked_role = discord.utils.get(guild.roles, name='Vibechecked')
            await ctx.send(f'{user.display_name} has been vibechecked.')
            await user.add_roles(vibechecked_role)

    @vibecheck.error
    async def vibecheck_error(self, ctx, error):
        guild = discord.utils.get(self.client.guilds, name='UNSW Discussion')
        if isinstance(error, discord.ext.commands.errors.NotOwner):
            vibechecked_role = discord.utils.get(guild.roles, name='Vibechecked')
            await ctx.message.author.add_roles(vibechecked_role)
        else:
            await ctx.send('Please try again.')

    @commands.command()
    @commands.is_owner()
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def nickname(self, ctx, user: discord.Member, *nicknames):
        guild = discord.utils.get(self.client.guilds, name='UNSW Discussion')
        channel = discord.utils.get(guild.text_channels, name="bot")
        if channel == ctx.message.channel:
            nickname = " ".join(nicknames)
            list_of_nicks = [str(member.nick).lower() for member in guild.members]
            if nickname.lower() in list_of_nicks:
                raise Exception
            await user.edit(nick=nickname)
            await ctx.send("Nickname changed")

    @nickname.error
    async def nickname_error(self, ctx, error):
        await ctx.send("It didn't work for some reason lol")

def setup(client):
    client.add_cog(Mod(client))
