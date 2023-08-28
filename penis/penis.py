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
    async def peni_custom(self, ctx, user: discord.Member, customMsg):
        """Custom Size/Message

        You can customize how large a certain user is, or give them a custom string as their size.
        """

        customs = await self.config.customs()

        # Check if user is already in dict
        if user.id in customs.keys():
            await ctx.send(f"{user} ({user.id}) is added")
        else:
            await ctx.send(f"{user} ({user.id}) is not added")

            # let's add it
            customs.update({user.id: customMsg})
            await self.config.customs.set(customs)

            await ctx.send(f"{user} ({user.id}) added with custom message: {customMsg}")


        
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