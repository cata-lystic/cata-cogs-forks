import discord
import random
from redbot.core.bot import Red
from redbot.core import Config, commands, checks
from redbot.core.utils.chat_formatting import pagify


class Penis(commands.Cog):
    """Penis related commands."""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=18523712923481, force_registration=True)

        default_global = {
            "customs": {
                "514556311573364746": 29
            }
        }

        self.config.register_global(**default_global)

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

        customs = await self.config.customs()

        for user in users:
            random.seed(str(user.id))
            userID = str(user.id)

            if ctx.bot.user.id == user.id:
                dongs[user] = "8{}D".format("=" * 50)
            elif (userID in customs):
                userMsg = str(customs[userID])
                if userMsg.isdigit():
                    length = int(userMsg)
                    dongs[user] = "8{}D".format("=" * length)
                else:
                    dongs[user] = customs[userID]
            else:
                length = random.randint(0, 30)
                dongs[user] = "8{}D".format("=" * length)

        random.setstate(state)
        #dongs = sorted(dongs.items(), key=lambda x: x[1]) old sorting
        dongs = sorted(dongs.items(), key=lambda x: len(x[1]), reverse=True)

        for user, dong in dongs:
            msg += "**{}'s size:**\n{}\n".format(user.display_name, dong)

        for page in pagify(msg):
            await ctx.send(f"{page}")
            
    @commands.group(name='peniset', aliases=['penisset'])
    @checks.is_owner()
    async def peniset(self, ctx):
        """Penis Settings"""

    @peniset.command(name='custom')
    async def peni_custom(self, ctx, user: discord.Member, *, customMsg = None):
        """Custom Size/Message

        You can customize how large a certain user is, or give them a custom string as their size.
        """
        customs = await self.config.customs()
        userID = str(user.id)

        # if they didn't put a message, show them current custom message
        if customMsg == "" or customMsg == None:
            if (userID in customs):
                current = customs[userID]
                return await ctx.send(f"{user} current message: {current}")
            else:
                return await ctx.send(f"{user} does not currently have a message")

        # let's add/change it
        customs.update({userID: str(customMsg)})
        await self.config.customs.set(customs)
        msgType = "size" if customs[userID].isdigit() else "message"

        await ctx.send(f"{user} ({userID}) custom {msgType} set: {customMsg}")

    @peniset.command(name='enlarge', aliases=['en'])
    async def peni_enlarge(self, ctx, user: discord.Member, amount=1):
        """Enlarge User

        You can add size to a user's penis
        Example (Add 1): [p]peniset enlarge @User
        Example (Add 3): [p]peniset enlarge @User 3
        """
        customs = await self.config.customs()
        userID = str(user.id)

        # Check if user is already in customs
        # If so, check if it's a number or a message
        # If it's a number, add to it
        # If it's a message, tell OP they can't enlarge a custom message
        # If user is not in customs yet, calculate what their normal size would be and add amount to it
        if userID in customs:

            current = str(customs[userID])

            if current.isdigit():
                current = int(current) + int(amount)
                customs[userID] = current
                await self.config.customs.set(customs)
                return await ctx.send(f"{user}'s size has grown to {current}.")
            else:
                return await ctx.send(f"{user} has a custom message, you can't enlarge/shrink them.")
        
        else:

            random.seed(str(user.id))
            length = random.randint(0, 30)

            current = int(length) + int(amount)
            customs[userID] = current
            await self.config.customs.set(customs)
            return await ctx.send(f"{user}'s size has grown to {current}.")

    @peniset.command(name='clear', aliases=['cl'])
    async def peni_clear(self, ctx, user: discord.Member):
        """Clear User

        Reset user's penis to its original size.

        Example: [p]peniset clear @User
        """
        customs = await self.config.customs()
        userID = str(user.id)

        if userID in customs:
            del customs[userID]
            await self.config.customs.set(customs)
            return await ctx.send(f"{user}'s original size has been set.")
        else:
            return await ctx.send(f"{user}'s original size is already set.")
