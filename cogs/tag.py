# import discord
# from discord.ext import commands
# from aioconsole import ainput
#
#
# class Tag(commands.Cog):
#
#     def __init__(self, client):
#         self.client = client
#
#     @commands.command()
#     @commands.is_owner()
#     async def tag(self, ctx, channel_name: str):
#         guild = discord.utils.get(self.client.guilds, name='USyd Discussion')
#         channel = discord.utils.get(guild.text_channels, name=channel_name)
#         print('\nStudent Centre can now speak at #{}'.format(channel.name))
#         await ctx.send("You have control.")
#         while True:
#             msg = await ainput("What is the message: ")
#             if msg == '?exit':
#                 print("Student Centre is no longer speaking at #{}".format(channel.name))
#                 break
#             await channel.send(msg)
#
#     @tag.error
#     async def tag_error(self, ctx, error):
#         if isinstance(error, discord.ext.commands.errors.NotOwner):
#             await ctx.send('Bruh! The latency is {}ms.'.format(round(self.client.latency * 1000)))
#         else:
#             await ctx.send('Please try again.')
#
#
# def setup(client):
#     client.add_cog(Tag(client))
