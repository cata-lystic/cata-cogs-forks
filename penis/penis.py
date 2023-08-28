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
            "customs": {},
            "defaultLeaderboard": "custom",
            "defaultLeaderboardSort": "large"
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

            # Check if userID is in customs
            if (userID in customs):
                userMsg = str(customs[userID])

                # Check if length is number
                try:
                    int(userMsg)
                    length = int(userMsg)
                    dongs[user] = self.outputDong(self, length) # parse dong
                # Otherwise it's a custom message
                except ValueError:
                    dongs[user] = customs[userID]
            # If not, output user's default/original dong size
            # this is based on a static seed so user's default size will never change
            else:
                length = self.originalSize(self, user)
                dongs[user] = self.outputDong(self, length)

                # Set this in the customs dict for leaderboards
                customs[userID] = length
                await self.config.customs.set(customs)

        random.setstate(state)
        #dongs = sorted(dongs.items(), key=lambda x: x[1]) old sorting

        # Sort dongs by longest to shortest
        dongs = sorted(dongs.items(), key=lambda x: len(x[1]), reverse=True)

        # Make text list of each user's size 
        for user, dong in dongs:
            msg += "**{}'s size:**\n{}\n".format(user.display_name, dong)

        # Output results
        for page in pagify(msg):
            await ctx.send(f"{page}")

    @commands.command(name='penisboard')
    # list can be 'custom', 'small' or 'natural'
    async def penisboard(self, ctx, list="custom", sort="large"):
        """Penis Leaderboard"""

        # Make sure arguments are valid
        if list not in ['custom', 'natural', 'small']:
            return await ctx.send("Error: List must be `custom`, `natural`, or `small`")
        if sort not in ['large', 'small']:
            return await ctx.send("Error: Sort must be `large` or `small`")

        customs = await self.config.customs()

        guild = ctx.guild
        dongs = {}
        
        # remove from dict if isn't a number
        for cust in customs:
            
            userID = cust
            if int(ctx.bot.user.id) == int(userID):
                continue # don't show bot on leaderboard
            userLength = customs[cust]
            member = guild.get_member(int(userID))

            if not member:
                continue # don't show users that have left guild

            # Custom leaderboard (calc custom sizes)
            if list == "custom" or list == "small":

                # Check if userLength is actually a number, not custom string
                try:
                    int(userLength)
                    dongs[member] = int(userLength)
                except ValueError:
                    doNothing = True

                listName = "" # don't prefix 'Penis Leaderboard' for custom
                
            # Natural leaderboard (calc original sizes)
            else:
                dongs[member] = self.originalSize(self, member)
                listName = "Natural "

        sortName = "Small " if sort == "small" or list == "small" else ""
        sortOrder = False if sort == "small" or list == "small" else True
        dongs = sorted(dongs.items(), key=lambda x: int(x[1]), reverse=sortOrder)
        msg = f"`{sortName}{listName}Penis Leaderboard`\n"
        x = 0
        for user, dong in dongs:
            if x == 10:
                break
            msg += "**{}:** {}\n".format(user, dong)
            x += 1

        for page in pagify(msg):
            await ctx.send(f"{page}")

            
            
    @commands.group(name='peniset', aliases=['penisset'])
    @checks.mod_or_permissions()
    async def peniset(self, ctx):
        """Penis Settings"""

    @peniset.command(name='custom')
    async def peni_custom(self, ctx, user: discord.Member, *, customMsg = None):
        """Set a custom size or message for a user.

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

    @peniset.command(name='adjust', aliases=['enlarge', 'shrink'])
    async def peni_adjust(self, ctx, user: discord.Member, amount=1):
        """Enlarge or shrink user's penis size.

        You can add size to a user's penis
        Example (Add 1): [p]peniset adjust @User
        Example (Add 3): [p]peniset adjust @User 3
        Example (Rem 2): [p]peniset adjust @User -2
        """
        customs = await self.config.customs()
        userID = str(user.id)

        # Check if growing or shrinking
        

        # Check if user is already in customs
        if userID in customs:

            current = str(customs[userID]) # current length

            # check if current val is a number and not a string
            try:
                int(current)
                length = int(current) + int(amount)
            # if string, tell user this can't be adjust
            except ValueError:
                return await ctx.send(f"{user} has a custom message, you can't adjust them.")
        # If not, get original size
        else:
            length = self.originalSize(self, user)
        
        adjustment = "shrunk" if str(amount).startswith("-") else "grown"
        length = 0 if length < 0 else length # don't let it go below 0
        customs[userID] = length
        await self.config.customs.set(customs)
        return await ctx.send(f"{user}'s size has {adjustment} to {length}.")

    @peniset.command(name='clear', aliases=['cl'])
    async def peni_clear(self, ctx, user: discord.Member):
        """Reset user's penis to its original size.

        Example: [p]peniset clear @User
        """
        customs = await self.config.customs()
        userID = str(user.id)
        originalSize = self.originalSize(self, user)

        if userID in customs:
            del customs[userID]
            await self.config.customs.set(customs)
            return await ctx.send(f"{user}'s original size ({originalSize}) has been set.")
        else:
            return await ctx.send(f"{user}'s original size ({originalSize}) is already set.")
        
    @peniset.command(name='defaultleaderboard')
    async def peni_leaderboard_default(self, ctx, val):
        """Set default leaderboard.

        Example: [p]peniset defaultleaderboard natural
        Example: [p]peniset defaultleaderboard custom
        Example: [p]peniset defaultleaderboard small
        """

        if val not in ['custom', 'natural', 'small']:
            return await ctx.send("Error: defaultleaderboard can only be `custom`, `natural`, or `small`")
        
        await self.config.defaultLeaderboard.set(val)
        return await ctx.send(f"Default leaderboard set to  `{val}`")
        
    # Calculate the size if just using the original Python seed for random number.
    def originalSize(self, ctx, user: discord.member):
        random.seed(str(user.id))
        userID = str(user.id)

        if ctx.bot.user.id == user.id:
            return 50
        else:
            return random.randint(0, 30)
        
    def outputDong(self, ctx, length):
        return "8{}D".format("=" * length)
    