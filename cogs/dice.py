from discord.ext import commands
from secrets import randbelow


class Dice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question: commands.clean_content):
        answers = (
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        )

        # cryptographically secure RNG because why not
        answer = answers[randbelow(len(answers))]

        response = f"Question: {question}\nAnswer: {answer}"
        await ctx.send(response)


def setup(client):
    client.add_cog(Dice(client))
