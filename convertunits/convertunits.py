import discord
from redbot.core.bot import Red
from redbot.core import Config, commands

class Convertunits(commands.Cog):
    """Convert Units"""

    __author__ = "Cata-lystic"
    __version__ = "0.1"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=13374488281923, force_registration=True)

        default_global = {
            "round": 10,
            "excluded": []
        }

        self.config.register_global(**default_global)

        """
        List of valid units
        
        The First two values in the unit keyword's list are the singular and plural
        versions of the unit. These will be used in the final output

        Note: Always include the keyword in the list
        """
        self.valid = {
            'weight': {
                'lb': ['pound', 'pounds', 'lb', 'lbs'],
                'oz': ['ounce', 'ounces', 'oz', 'os'],
                'kg': ['kilogram', 'kilograms', 'kg', 'kgs', 'kilo', 'kilos'],
                'gr': ['gram', 'grams', 'gr', 'grm'],
                'ton': ['ton', 'tons', 'uston'],
                'tonne': ['tonne', 'tonnes', 'ukton']
            },
            'temp': {
                'c': ['Celsius', 'Celsius', 'c', 'celsius', 'cel'],
                'f': ['Fahrenheit', 'Fahrenheit', 'f', 'fahrenheit', 'fah'],
                'k': ['Kelvin', 'Kelvin', 'k', 'kelvin', 'kelv', 'kel']
            },
            'distance': {
                'ft': ['foot', 'feet', 'ft', 'feets', 'foots'],
                'in': ['inch', 'inches', 'in'],
                'me': ['meter', 'meters', 'me', 'met'],
                'cm': ['centimeter', 'centimeters', 'cm', 'centi'],
                'mm': ['millimeter', 'millimeters', 'mm', 'millim'],
                'mi': ['mile', 'miles', 'mi'],
                'km': ['kilometer', 'kilometers', 'km', 'kilom']
            },
            'liquid': {
                'gal': ['gallon', 'gallons', 'gal', 'gals'],
                'floz': ['fluid ounce', 'fluid ounces', 'floz', 'flo', 'flz', 'fluidounce', 'fluidounces'],
                'qt': ['quart', 'quarts', 'qt'],
                'pint': ['pint', 'pints', 'pi', 'pin', 'pnt'],
                'cup': ['cup', 'cups', 'cp'],
                'lit': ['liter', 'liters', 'lit'],
                'ml': ['milliliter', 'milliliters', 'ml', 'millil']
            }
        }

        # force convertTo to be whichever the opposite of the single value command is
        self.forceList = {
            'c': 'f', 'f': 'c',         # Celsius/Fahrenheit
            'mi': 'km', 'km': 'mi',     # Miles/Kilometers
            'lb': 'kg', 'kg': 'lb',     # Pounds/Kilograms
            'gal': 'lit', 'lit': 'gal', # Gallons/Liters
            'in': 'cm', 'cm': 'in',     # Inches/Centimeters
            'ft': 'me', 'me': 'ft'      # Feet/Meters
        }
        

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Convert Help"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"
    

    @commands.command(name="example")
    async def example_command(self, ctx, something):
        await ctx.send("This is an example command.")

    @commands.command(name="change_help")
    async def change_help_command(self, ctx):
        command = self.bot.get_command("example")
        command.help = "This is the updated help description."
        await ctx.send("The help description for the 'example' command has been updated.")

    def convHelpMenu():
        # List each available unit
        msg = ""
        for category, subdict in self.valid.items():
            msg += f"Category: {category}"
            for unit, aliases in subdict.items():
                msg += (", ".join(map(str, unit)))


    @commands.command(aliases=['con', 'convertunits'], help=convHelpMenu())
    async def conv(self, ctx: commands.Context, convertFrom, convertTo, val: float=1):
        """Convert Units
        
        **Weight**
        `lb` Pounds, `kg` Kilograms, `oz` Ounces
        `gr` Grams, `ton` Tons (US), `tonne` Tonnes (UK)
        **Distance**
        `ft` Feet, `me` Meters, `in` Inches, `mm` Millimeters
        `cm` Centimeters, `mi` Miles, `km` Kilometers
        **Liquid**
        `gal` Gallons, `lit` Liters, `floz` Fluid Ounces
        `cup` Cups, `qt` Quarts, `pint` Pints, `ml` Milliliters
        **Temperature**
        `c` Celsius, `f` Fahrenheit, `k` Kelvin
        
        **Examples**
        .conv lb kg 45
        .conv c 30"""        

        # Check if convertTo is a number/float
        # If it is, use convertTo as the val
        # This is because c, f, mi, and km don't require a convertTo
        try:
            float(convertTo)

            val = float(convertTo)

            convertTo = self.forceList[convertFrom]

        except ValueError:
            pass

        if (convertFrom == convertTo):
            return await ctx.send("You can't convert the same unit")

        # Loop through each list in the dictionary and see if it exists.
        # if it does, return the index

        validFrom = "" # Converting from
        validTo = "" # Converting to
        categoryFrom = "" # Conversion category
        categoryTo = ""
        errorMsg = ""

        # Loop through 'valid' dictionary to see if convertFrom and convertTo
        # match a value in the subdict
        for cat, vals in self.valid.items():

            # Check to make sure chosen conversions are valid
            key_list = list(self.valid[cat].keys())
            val_list = list(self.valid[cat].values())

            for i in range(len(val_list)):
                if convertFrom in val_list[i]:
                    validFrom = key_list[i]
                    categoryFrom = cat

                if convertTo in val_list[i]:
                    validTo = key_list[i]
                    categoryTo = cat

        excluded = await self.config.excluded()
        if any(s in excluded for s in [validFrom, validTo]):
            errorMsg = f"Error: One or more chosen units is excluded."
        elif validFrom == "":
            errorMsg = f"Error: `{convertFrom}` is not a valid unit."
        elif validTo == "":
            errorMsg = f"Error: `{convertTo}` is not a valid unit."
        elif categoryFrom != categoryTo or categoryFrom == "" or categoryTo == "":
            errorMsg = f"Error: Cannot convert from `{categoryFrom}` to `{categoryTo}`."
        else:
            final = f"{validFrom} {validTo}"

        # Return error if found
        if errorMsg != "":
            return await ctx.send(errorMsg)
        
        calc = await self.formula(validFrom, validTo, val)

        if calc != None:
            plural1 = 1 if val != 1 else 0
            plural2 = 1 if calc != 1 else 0
            con1 = self.valid[categoryTo][validFrom][plural1]
            con2 = self.valid[categoryTo][validTo][plural2]
            msg = ("> {val} {con1} is equal to {calc} {con2}.").format(val=val, calc=calc, con1=con1, con2=con2)
        else:
            msg = "Invalid set of conversions."

        return await ctx.send(f"{msg}")

    # Functions
    @commands.group(name='convset')
    async def convset(self, ctx):
        """Convertunits Settings
        
        Test"""

    @convset.command(name='round')
    async def conv_round(self, ctx, val: int):
        """Set max decimal point to round up to.
        Example: .convset round 4
        """
        
        await self.config.round.set(val)
        return await ctx.send(f"Round set to {val}")
    
    @convset.command(name='showsettings')
    async def conv_showsettings(self, ctx):
        """Current Settings
        """
        msg = "**Current Settings**\n"

        round = await self.config.round()
        msg += f"Round: {round}\n"

        msg += "Excluded: "
        excluded = await self.config.excluded()
        msg += (", ".join(map(str, excluded)))

        return await ctx.send(msg)

    
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

        

    @convset.command(name='exclude', aliases=['disable', 'ex', 'dis', 'rem', 'remove'])
    async def conv_disable(self, ctx, command):
        """Exclude unit from available choices.

        You can remove any unit from being accessible.

        Example: .convset exclude k
        """

        # Check if command is already excluded
        if self.isExcluded(self, command) == True:
            return ctx.send(f"`{command}` is already excluded.")

        # Make sure this is a valid command
        isValid = await self.isValid(self, command)
                
        # Unit is invalid, show valid units
        if isValid == False:
            units = await self.listValidUnits(self)
            return await ctx.send(f"`{command}` is not a valid unit.\nUnits: {units}")
        
        # Unit is valid, add to excluded list
        current = await self.config.excluded()
        current.append(command) # add to list

        await self.config.excluded.set(current) # save
        return await ctx.send(f"`{command}` excluded.")
    
    @convset.command(name='include', aliases=['enable', 'en', 'in', 'add', 'inc'])
    async def conv_include(self, ctx, command):
        """Include unit from available choices.

        You can include units that you previously excluded here. 

        Example: .convset include k
        """

        # Make sure this is a valid command
        isValid = await self.isValid(command)

        # Unit is invalid, show valid units
        if isValid == False:
            units = await self.listValidUnits(self)
            return await ctx.send(f"`{command}` is not a valid unit.\nUnits: {units}")

        # Unit is valid, remove from excluded list
        current = await self.config.excluded()
        if command in current:
            current.remove(command) # remove from list
            await self.config.excluded.set(current) # save
            return await ctx.send(f"`{command}` included.")
        else:
            return await ctx.send(f"`{command}` is not excluded.")

    # Formula (Calculate conversion)
    async def formula(self, convFrom, convTo, val: float):

        # Combine units
        units = f"{convFrom} {convTo}"

        formulas = {
            "lb kg": val * 0.45359237, # Pounds
            "lb oz": val * 16,
            "lb gr": val * 453.592,
            "lb ton": val / 2000,
            "lb tonne": val / 2204.62,
            "kg lb": val / 0.45359237, # Kilograms
            "kg oz": val * 35.2739619,
            "kg gr": val * 1000,
            "kg ton": val / 907.185,
            "kg tonne": val / 1016.05,
            "gr lb": val / 453.592, # Grams
            "gr kg": val / 1000,
            "gr oz": val / 28.3495,
            "gr ton": val / 907185,
            "gr tonne": val / 1016000,
            "oz lb": val / 16, # Ounces
            "oz kg": val / 35.274,
            "oz gr": val * 28.35,
            "oz ton": val / 32000,
            "oz tonne": val / 35840,
            "ton lb": val * 2000, # Tons (US)
            "ton kg": val * 907.185,
            "ton oz": val * 32000,
            "ton gr": val * 907185,
            "ton tonne": val * 0.892857, # Tonnes (UK)
            "tonne lb": val * 2240,
            "tonne kg": val * 1016.05,
            "tonne oz": val * 35840,
            "tonne gr": val * 1016050,
            "tonne ton": val * 1.12,
            "f c": round((val - 32) / 1.8, 1), # Fahrenheit
            "f k": (val + 459.67) * 5/9,
            "c f": round((val * 1.8) + 32, 1), # Celsius
            "c k": val + 273.15,
            "k c": val - 273.15,
            "k f": val * 9/5 - 459.67,
            "ft me": val * 0.3048, # Feet
            "ft cm": val * 30.48,
            "ft in": val * 12,
            "ft mi": val / 5280,
            "ft km": val * 0.0003048,
            "ft mm": val * 304.8,
            "me ft": val * 3.28084, # Meters
            "me cm": val * 100,
            "me in": val * 39.37,
            "me mi": val * 0.000621371,
            "me km": val / 1000,
            "me mm": val * 1609344,
            "cm ft": val / 30.48, # Centimeters
            "cm me": val / 100,
            "cm in": val / 2.54,
            "cm mi": val * 0.0000062137,
            "cm km": val / 100000,
            "cm mm": val * 10,
            "in ft": val / 12, # Inches
            "in me": val * 0.0254,
            "in cm": val * 2.54,
            "in mi": val * 0.000015783,
            "in km": val * 0.0000254,
            "in mm": val * 25.4,
            "mi km": val * 1.609344, # Miles
            "mi me": val * 1609.344,
            "mi ft": val * 5280,
            "mi cm": val * 160934.4,
            "mi in": val * 63360,
            "mi mm": val * 1609344,
            "km mi": val * 0.621371, # Kilometers
            "km me": val * 1000,
            "km ft": val * 3280.84,
            "km cm": val * 100000,
            "km in": val * 39370.1,
            "km mm": val * 1000000,
            "mm mi": val / 1609344, # Millimeters
            "mm km": val / 1000000,
            "mm ft": val * 0.00328084,
            "mm cm": val / 10,
            "mm in": val * 0.0393701,
            "mm me": val / 1000,
            "gal lit": val * 3.78541, # Gallons
            "gal floz": val * 128,
            "gal cup": val * 16,
            "gal pint": val * 8,
            "gal qt": val * 4,
            "gal ml": val * 3785.411784,
            "lit gal": val * 0.264172, # Liters
            "lit floz": val * 33.814,
            "lit cup": val * 4.22675,
            "lit pint": val * 2.11337642,
            "lit qt": val / 1.05668821,
            "lit ml": val * 1000,
            "floz gal": val / 128, # Fluid Ounces
            "floz lit": val / 33.814,
            "floz cup": val / 8,
            "floz pint": val / 16,
            "floz qt": val / 32,
            "floz ml": val * 29.5735296,
            "cup gal": val * 0.0625, # Cups
            "cup lit": val * 0.236588,
            "cup floz": val * 8,
            "cup pint": val / 2,
            "cup qt":  val / 4,
            "cup ml": val * 236.5882365,
            "qt gal": val / 4, # Quarts
            "qt lit": val * 0.946353,
            "qt pint": val * 2,
            "qt cup": val * 4,
            "qt floz": val * 32,
            "qt ml": val * 946.352946,
            "pint gal": val / 8, # Pints
            "pint lit": val * 0.473176,
            "pint cup": val * 2,
            "pint floz": val * 16,
            "pint qt": val / 2,
            "pint ml": val * 473.176473,
            "ml gal": val * 0.000264172, # Milliliters
            "ml lit": val / 1000,
            "ml floz": val * 0.033814,
            "ml qt": val / 946.352946,
            "ml pint": val * 0.0021133764,
            "ml cup": val / 236.5882365
        }

        rounding = await self.config.round()

        if units in formulas:
            return round(formulas[units], rounding)
        else:
            return None
    