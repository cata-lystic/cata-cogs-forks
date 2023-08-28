import discord
import random
from redbot.core.bot import Red
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import pagify


class Penis(commands.Cog):
    """Penis related commands."""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=18523712923481, force_registration=True)

        default_global = {
            "customs": {
                514556311573364746: "WEEE"
            },
            "enlarge": {
                514556311573364746: 1
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

        #dorks = {
        #    1019025452511277116: "8[][][D", # Bean
        #    441088103826980885: "{()}", # Sophist
        #    477936660684996639: "~", # Geko
        #    514556311573364746: "<('‿')>" # Catalyst
        #}

        customs = await self.config.customs()

        for user in users:
            random.seed(str(user.id))
            userID = str(user.id)

            if ctx.bot.user.id == user.id:
                dongs[user] = "8{}D".format("=" * 50)
            elif (userID in customs):
                if isinstance(customs[userID], int):
                    length = customs[userID]
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
            
    @commands.group(name='peniset')
    async def peniset(self, ctx):
        """Convertunits Settings
        
        Test"""

    @peniset.command(name='custom')
    async def peni_custom(self, ctx, user: discord.Member, customMsg = None):
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

        await ctx.send(f"{user} ({userID}) custom message set: {customMsg}")


        
        #await self.config.custom.set(val)


    # Check if command is already excluded
    async def isExcluded(self, ctx, command):
        excluded = await self.config.excluded()
        if command in excluded:
            return True
        else:
            return False
    
    # Check if unit is valid
    async def isValid(self, ctx, command):
        isValid = False
        for key, subdict in self.valid.items():
            if command in subdict:
                isValid = True
        return isValid
    
    async def listValidUnits(self, ctx):
        msg = ""
        for key, value in self.valid.items():
            msg += (", ".join(value.keys())+" ")
        return msg