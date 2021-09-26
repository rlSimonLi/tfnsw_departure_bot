import discord
from discord.ext import commands


class Role(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_faculty_by_emote(emote, guild):
        roles = {
            '🎨': 'Arts and Social Sciences',
            '🔬': 'Science',
            '💊': 'Medicine and Health',
            '⚖️': 'Law',
            '🏙️': 'Architecture, Design and Planning',
            '🎵': 'Music',
            '💵': 'Business',
            '🚀': 'Engineering'
        }
        if emote.name not in roles:
            return None
        else:
            return discord.utils.get(guild.roles, name=roles[emote.name])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
        role = None

        # the rule agreement
        if message_id == 667344953600507905:
            if payload.emoji.name == '3️⃣':
                role = discord.utils.get(guild.roles, name='Philosopher')

        # faculty role
        if message_id == 667382793751494666:
            role = Role.get_faculty_by_emote(payload.emoji, guild)

        if role:
            member = await guild.fetch_member(payload.user_id)
            if len(member.roles) <= 5:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
        role = None

        # the rule agreement
        if message_id == 667344953600507905:
            if payload.emoji.name == '3️⃣':
                role = discord.utils.get(guild.roles, name='Philosopher')

        # faculty role
        if message_id == 667382793751494666:
            role = Role.get_faculty_by_emote(payload.emoji, guild)

        if role:
            member = await guild.fetch_member(payload.user_id)
            await member.remove_roles(role)

    @commands.command()
    @commands.is_owner()
    async def add_verification_reacts(self, ctx, channel_name: str, msg_id: int):
        guild = discord.utils.get(self.client.guilds, name='USYD Discussion')
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        message = await channel.fetch_message(msg_id)
        reacts = ['9️⃣', '⬆️', '⏯️', '6️⃣', '8️⃣', '3️⃣', '➡️', '⏫', '2️⃣', '🔢', '1️⃣', '🔟', '🔼', '⏩', '#️⃣', '4️⃣', '5️⃣', '⏭️', '0️⃣', '7️⃣']
        for react in reacts:
            await message.add_reaction(react)

    @commands.command()
    @commands.is_owner()
    async def add_faculty_reacts(self, ctx, channel_name: str, msg_id: int):
        guild = discord.utils.get(self.client.guilds, name='USYD Discussion')
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        message = await channel.fetch_message(msg_id)
        reacts = ['🎨', '🔬', '💊', '⚖️', '🏙️', '🎵', '💵', '🚀']
        for react in reacts:
            await message.add_reaction(react)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = "Hi! Welcome to the USYD Discussion Server!\n\nTo unlock the rest of the server, please read the " \
              "**#rules**. We have also included a compilation of **#useful_links** related to the university. If you " \
              "would like, you can introduce yourself in **#introduction**. "
        await member.send(msg)

def setup(client):
    client.add_cog(Role(client))
