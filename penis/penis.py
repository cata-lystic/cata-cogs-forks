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

        for user in users:
            random.seed(str(user.id))

            if ctx.bot.user.id == user.id:
                dongs[user] = "8{}D".format("=" * 50)
            elif user.id == 1019025452511277116:
                dongs[user] = "8[][][D"
            elif user.id == 441088103826980885:
                dongs[user] = "{()}"
            else:
                length = random.randint(0, 30)
                dongs[user] = "8{}D".format("=" * length)

        random.setstate(state)
        sorted_values = sorted(dongs.values(), key=lambda x: len(x))
        sorted_dongs = {k: v for v, k in zip(sorted_values, dongs.keys())}

        #dongs = sorted(dongs.items(), key=lambda x: x[1])
        #dongs = sorted(dongs.items(), key=len)

        for user, dong in sorted_dongs:
            msg += "**{}'s size:**\n{}\n".format(user.display_name, dong)

        for page in pagify(msg):
            await ctx.send(page)
            