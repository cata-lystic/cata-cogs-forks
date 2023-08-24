import discord

from redbot.core.bot import Red
from redbot.core import commands
#from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import humanize_timedelta

from typing import Union
from datetime import datetime, timezone

import contextlib

#_ = Translator("Converters", __file__)


#@cog_i18n(_)
class Converters(commands.Cog):
    """Convert Units"""

    __author__ = "Cata-lystic"
    __version__ = "0.1"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Convert Help"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    # List aliases
    @commands.command()
    async def convs(self, ctx):
        await ctx.send(f"# Conversions\n`.c` - Celsius to Fahrenheit\n`.f` - Fahrenheit to Celsius\n`.ft` - Feet to Meters, `.ftcm` to Centimeters, `.ftin` to Inches\n`.lb` - Pounds to Kilograms, `lboz` to Ounces, `.ftgr` to Grams\n`.kg` - Kilograms to Pounds, `kgoz` to Ounces, `.kggr` to Grams\n`.km` - Kilometers to Miles\n`.me` - Meters to Feet, `.mecm` to Centimeters, `.mein` to Inches\n`.mi` - Miles to Kilometers\n\nType `.conv` for the full help menu.")


    @commands.command(aliases=['con'])
    async def conv(self, ctx: commands.Context, convertFrom, convertTo, val: float=1):
        """Convert Units
        
        **Weight**
        `lb` Pounds, `kg` Kilograms, `oz` Ounces
        `gr` Grams, `ton` Tons (US), `tonne` Tonnes (UK)
        **Distance**
        `ft` Feet, `me` Meters, `in` Inches
        `cm` Centimeters, `mi` Miles, `km` Kilometers
        **Liquid**
        `gal` Gallons, `lit` Liters, `floz` Fluid Ounces
        `cup` Cups, `qt` Quarts, `pint` Pints
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

            # force convertTo to be whichever the opposite of the single value command is
            forceList = {
                'c': 'f',
                'f': 'c',
                'mi': 'km',
                'km': 'mi'
            }

            convertTo = forceList[convertFrom]

        except ValueError:
            pass

        if (convertFrom == convertTo):
            return await ctx.send("You can't convert the same unit")

        # List of valid conversions
        valid = {
            'weight': {
                'lb': ['pounds', 'lb', 'lbs', 'pound'],
                'kg': ['kilograms', 'kg', 'ki', 'kgs', 'kilo', 'kilos', 'kilogram'],
                'oz': ['ounces', 'oz', 'ounce', 'os'],
                'gr': ['grams', 'gr', 'gram'],
                'ton': ['tons', 'ton', 'uston'],
                'tonne': ['tonnes', 'tonne', 'ukton']
            },
            'temp': {
                'c': ['Celsius', 'c', 'celsius', 'cel'],
                'f': ['Fahrenheit', 'f', 'fahrenheit', 'fah'],
                'k': ['Kelvin', 'k', 'kelvin', 'kelv', 'kel']
            },
            'distance': {
                'ft': ['feet', 'ft', 'feets', 'foot', 'foots'],
                'me': ['meters', 'me', 'meter'],
                'in': ['inches', 'in', 'inch'],
                'cm': ['centimeters', 'cm', 'centi', 'centimeter'],
                'mi': ['miles', 'mi', 'mile'],
                'km': ['kilometers', 'km', 'kilometer, kilom']
            },
            'liquid': {
                'gal': ['gallons', 'gal', 'gals', 'gallon'],
                'lit': ['liters', 'lit', 'liter'],
                'floz': ['fluid ounces', 'floz', 'flo', 'flz', 'fluidounce', 'fluidounces'],
                'cup': ['cups', 'cup'],
                'qt': ['quarts', 'qt', 'quart'],
                'pint': ['pints', 'pint', 'pi']
            }
        }

        # Loop through each list in the dictionary and see if it exists.
        # if it does, return the index

        validFrom = "" # Converting from
        validTo = "" # Converting to
        categoryFrom = "" # Conversion category
        categoryTo = ""
        errorMsg = ""

        # Loop through 'valid' dictionary to see if convertFrom and convertTo
        # match a value in the subdict
        for cat, vals in valid.items():

            # Check to make sure chosen conversions are valid
            key_list = list(valid[cat].keys())
            val_list = list(valid[cat].values())

            for i in range(len(val_list)):
                if convertFrom in val_list[i]:
                    validFrom = key_list[i]
                    categoryFrom = cat

                if convertTo in val_list[i]:
                    validTo = key_list[i]
                    categoryTo = cat
        
        if validFrom == "":
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

        # Here is the massive if/elif statement for each possible conversion
        
        calc = ""

        # Pounds to kilograms
        if final == "lb kg":
            calc = val * 0.45359237
        # Pounds to ounces
        elif final == "lb oz":
            calc = val * 16
        # Pounds to grams
        elif final == "lb gr":
            calc = val * 453.592
        # Pounds to tons (US)
        elif final == "lb ton":
            calc = val / 2000
        # Pounds to tonnes (UK)
        elif final == "lb tonne":
            calc = val / 2204.62

        # Kilograms to pounds
        elif final == "kg lb":
            calc = val / 0.45359237
        # Kilograms to ounces
        elif final == "kg oz":
            calc = val * 35.2739619
        # Kilograms to grams
        elif final == "kg gr":
            calc = val * 1000
        # Kilograms to tons (US)
        elif final == "kg ton":
            calc = val / 907.185
        # Kilograms to tonnes (UK)
        elif final == "kg tonne":
            calc = val / 1016.05

        # Grams to kilograms
        elif final == "gr kg":
            calc = val / 1000
        # Grams to pounds
        elif final == "gr lb":
            calc = val / 453.592
        # Grams to ounces
        elif final == "gr oz":
            calc = val / 28.3495
        # Grams to tons (US)
        elif final == "gr ton":
            calc = val / 907185
        # Grams to tonnes (UK)
        elif final == "gr tonne":
            calc = val / 1016000

        # Ounces to pounds
        elif final == "oz lb":
            calc = val / 16
        # Ounces to kilograms
        elif final == "oz kg":
            calc = val / 35.274
        # Ounces to grams
        elif final == "oz gr":
            calc = val * 28.35
        # Ounces to tons (US)
        elif final == "oz ton":
            calc = val / 32000
        # Ounces to tonnes (UK)
        elif final == "oz tonne":
            calc = val / 35840

        # Tons (US) to pounds
        elif final == "ton lb":
            calc = val * 2000
        # Tons to kilograms
        elif final == "ton kg":
            calc = val * 907.185
        # Tons to ounces
        elif final == "ton oz":
            calc = val * 32000
        # Tons to grams
        elif final == "ton gr":
            calc = val * 907185
        # Tons to tonnes (UK)
        elif final == "ton tonne":
            calc = val * 0.892857

        # Tonnes (UK) to pounds
        elif final == "tonne lb":
            calc = val * 2240
        # Tonnes to kilograms
        elif final == "tonne kg":
            calc = val * 1016.05
        # Tonnes to ounces
        elif final == "tonne oz":
            calc = val * 35840
        # Tonnes to grams
        elif final == "tonne gr":
            calc = val * 1016050
        # Tonnes to tons (US)
        elif final == "tonne ton":
            calc = val * 1.12

        # Celsius to Fahrenheit
        elif final == "c f":
            calc = round((val * 1.8) + 32, 1)
        # Celsius to Kelvin
        elif final == "c k":
            calc = val + 273.15
        # Fahrenheit to Celsius
        elif final == "f c":
            calc = round((val - 32) / 1.8, 1)
        # Fahrenheit to Kelvin
        elif final == "f k":
            calc = (val + 459.67) * 5/9

        # Feet to meters
        elif final == "ft me":
            calc = val * 0.3048
        # Feet to centimeters
        elif final == "ft cm":
            calc = val * 30.48
        # Feet to inches
        elif final == "ft in":
            calc = val * 12
        # Feet to miles
        elif final == "ft mi":
            calc = val / 5280
        # Feet to kilometers
        elif final == "ft km":
            calc = val * 0.0003048

        # Meters to feet
        elif final == "me ft":
            calc = val * 3.28084
        # Meters to centimeters
        elif final == "me cm":
            calc = val * 100
        # Meters to inches
        elif final == "me in":
            calc = val * 39.37
        # Meters to miles
        elif final == "me mi":
            calc = val * 0.000621371
        # Meters to kilometers
        elif final == "me km":
            calc = val / 1000

        # Centimeters to feet
        elif final == "cm ft":
            calc = val / 30.48
        # Centimeters to meters
        elif final == "cm me":
            calc = val / 100
        # Centimeters to inches
        elif final == "cm in":
            calc = val / 2.54
        # Centimeters to miles
        elif final == "cm mi":
            calc = val * 0.0000062137
        # Centimeters to kilometers
        elif final == "cm km":
            calc = val / 100000

        # Inches to feet
        elif final == "in ft":
            calc = val / 12
        # Inches to meters
        elif final == "in me":
            calc = val * 0.0254
        # Inches to centimeters
        elif final == "in cm":
            calc = val * 2.54
        # Inches to miles
        elif final == "in mi":
            calc = val * 0.000015783
        # Inches to kilometers
        elif final == "in km":
            calc = val * 0.0000254

        # Miles to kilometers
        elif final == "mi km":
            calc = val * 1.609344
        # Miles to meters
        elif final == "mi me":
            calc = val * 1609.344
        # Miles to feet
        elif final == "mi ft":
            calc = val * 5280
        # Miles to centimeters
        elif final == "mi cm":
            calc = val * 160934.4
        # Miles to inches
        elif final == "mi in":
            calc = val * 63360

        # Kilometers to miles
        elif final == "km mi":
            calc = val * 0.621371
        # Kilometers to meters
        elif final == "km me":
            calc = val * 1000
        # Kilometers to feet
        elif final == "km ft":
            calc = val * 3280.84
        # Kilometers to centimeters
        elif final == "km cm":
            calc = val * 100000
        # Kilometers to inches
        elif final == "km in":
            calc = val * 39370.1

        # Gallons to liters
        elif final == "gal lit":
            calc = val * 3.78541
        # Gallons to fluid ounces
        elif final == "gal floz":
            calc = val * 128
        # Gallons to cups
        elif final == "gal cup":
            calc = val * 16
        # Gallons to pints
        elif final == "gal pint":
            calc = val * 8
        # Gallons to quarts
        elif final == "gal qt":
            calc = val * 4

        # Liters to gallons
        elif final == "lit gal":
            calc = val * 0.264172
        # Liters to fluid ounces
        elif final == "lit floz":
            calc = val * 33.814
        # Liters to cups
        elif final == "lit cup":
            calc = val * 4.22675
        # Liters to pints
        elif final == "lit pint":
            calc = val * 2.11337642
        # Liters to quarts
        elif final == "lit qt":
            calc = val / 1.05668821

        # Fluid ounces to gallons
        elif final == "floz gal":
            calc = val / 128
        # Fluid ounces to liters
        elif final == "floz lit":
            calc = val / 33.814
        # Fluid ounces to cups
        elif final == "floz cup":
            calc = val / 8
        # Fluid ounces to pints
        elif final == "floz pint":
            calc = val / 16
        # Fluid ounces to quarts
        elif final == "floz qt":
            calc = val / 32

        # Cups to gallons
        elif final == "cup gal":
            calc = val * 0.0625
        # Cups to liters
        elif final == "cup lit":
            calc = val * 0.236588
        # Cups to fluid ounces
        elif final == "cup floz":
            calc = val * 8
        # Cups to pints
        elif final == "cup pint":
            calc = val / 2
        # Cups to quarts
        elif final == "cup qt":
            calc = val / 4

        # Quarts to gallons
        elif final == "qt gal":
            calc = val / 4
        # Quarts to liters
        elif final == "qt lit":
            calc = val * 0.946353
        # Quarts to pints
        elif final == "qt pint":
            calc = val * 2
        # Quarts to cups
        elif final == "qt cup":
            calc = val * 4
        # Quarts to fluid ounces
        elif final == "qt floz":
            calc = val * 32

        # Pints to gallons
        elif final == "pint gal":
            calc = val / 8
        # Pints to liters
        elif final == "pint lit":
            calc = val * 0.473176
        # Pints to cups
        elif final == "pint cup":
            calc = val * 2
        # Pints to fluid ounces
        elif final == "pint floz":
            calc = val * 16
        # Pints to quarts
        elif final == "pint qt":
            calc = val / 2




        if calc != "":
            con1 = valid[categoryTo][validFrom][0]
            con2 = valid[categoryTo][validTo][0]
            msg = ("> {val} {con1} is equal to {calc} {con2}.").format(val=val, calc=calc, con1=con1, con2=con2)
        else:
            msg = "Invalid set of conversions."

        return await ctx.send(f"{msg}")
