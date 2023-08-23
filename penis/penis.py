import discord
import random
from redbot.core import commands
from redbot.core.utils.chat_formatting import pagify


class Penis(commands.Cog):
    """Penis related commands."""

    @commands.command()
    async def penis(self, ctx, *users: discord.Member):
        """Detects user's penis length

        This is 100% accurate.
        Enter multiple users for an accurate comparison!"""
        if not users:
            await ctx.send_help()
            return

        dongs = {}
        msg = ""
        state = random.getstate()

        dorks = {
            1019025452511277116: "8[][][D", # Bean
            441088103826980885: "{()}", # Sophist
            477936660684996639: "~", # Geko
            514556311573364746: "<('‿')>" # Catalyst
        }

        for user in users:
            random.seed(str(user.id))

            if ctx.bot.user.id == user.id:
                dongs[user] = "8{}D".format("=" * 50)
            elif (user.id in dorks):
                dongs[user] = dorks[user.id]
            else:
                length = random.randint(0, 30)
                dongs[user] = "8{}D".format("=" * length)

        random.setstate(state)
        #dongs = sorted(dongs.items(), key=lambda x: x[1])
        dongs = sorted(dongs.items(), key=lambda x: len(x[1]), reverse=True)

        for user, dong in dongs:
            msg += "**{}'s size:**\n{}\n".format(user.display_name, dong)

        for page in pagify(msg):
            await ctx.send(f"{page}")
            