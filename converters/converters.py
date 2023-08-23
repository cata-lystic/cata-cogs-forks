import discord

from redbot.core.bot import Red
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import humanize_timedelta

from typing import Union
from datetime import datetime, timezone

import contextlib

_ = Translator("Converters", __file__)


@cog_i18n(_)
class Converters(commands.Cog):
    """Some converters."""

    __author__ = "Predä"
    __version__ = "0.3.10"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    # List aliases
    @commands.command()
    async def convs(self, ctx):
        await ctx.send(f"# Conversions\n`.c` - Celsius to Fahrenheit\n`.f` - Fahrenheit to Celsius\n`.ft` - Feet to Meters, `.ftcm` to Centimeters, `.ftin` to Inches\n`.lb` - Pounds to Kilograms, `lboz` to Ounces, `.ftgr` to Grams\n`.kg` - Kilograms to Pounds, `kgoz` to Ounces, `.kggr` to Grams\n`.km` - Kilometers to Miles\n`.me` - Meters to Feet, `.mecm` to Centimeters, `.mein` to Inches\n`.mi` - Miles to Kilometers\n\nType `.conv` for the full help menu.")


    # This is work on a unified command that will allow any values to be input and calculated as long as they belong to the same category.

    # Instead of a separate menu item for each measurement, commands will be taken like
    # .con gal lit  // true, gallons and liters can be converted
    # .con cm in    // true, centimeters and inches can be converted
    # .con gal in   // false, gallons and inches can't be converted




    @commands.command()
    async def con(self, ctx: commands.Context, convertFrom, convertTo, val: float=1):
        """Master converter.
        
        Weight: lb, kg, oz, gr, ton, tonne
        
        Temp: c, f"""

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
                'c': ['Celsius', 'c', 'celsius'],
                'f': ['Fahrenheit', 'f', 'fahrenheit']
            },
            'distance': {
                'ft': ['feet', 'ft', 'feets', 'foot', 'foots'],
                'me': ['meters', 'me', 'meter'],
                'in': ['inches', 'in', 'inch'],
                'cm': ['centimeters', 'cm', 'centi', 'centimeter']
            },
            'liquid': {
                'gal': ['gallons', 'gal', 'gals', 'gallon']'],
                'lit': ['liters', 'lit', 'liter'],
                'floz': ['fluid ounces', 'floz', 'fluidounce', 'fluidounces'],
                'cup': ['cups', 'cup']
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
        # Fahrenheit to Celsius
        elif final == "f c":
            calc = round((val - 32) / 1.8, 1)

        # Feet to meters
        elif final == "ft me":
            calc = val * 0.3048
        # Feet to centimeters
        elif final == "ft cm":
            calc = val * 30.48
        # Feet to inches
        elif final == "ft in":
            calc = val * 12

        # Meters to feet
        elif final == "me ft":
            calc = val * 3.28084
        # Meters to centimeters
        elif final == "me cm":
            calc = val * 100
        # Meters to inches
        elif final == "me in":
            calc = val * 39.37

        # Centimeters to feet
        elif final == "cm ft":
            calc = val / 30.48
        # Centimeters to meters
        elif final == "cm me":
            calc = val / 100
        # Centimeters to inches
        elif final == "cm in":
            calc = val / 2.54

        # Inches to feet
        elif final == "in ft":
            calc = val / 12
        # Inches to meters
        elif final == "in me":
            calc = val * 0.0254
        # Inches to centimeters
        elif final == "in cm":
            calc = val * 2.54

        # Gallons to liters
        elif final == "gal lit":
            calc = val * 3.78541
        # Gallons to fluid ounces
        elif final == "gal floz":
            calc = val * 128
        # Gallons to cups
        elif final == "gal cup":
            calc = val * 16

        # Liters to gallons
        elif final == "lit gal":
            calc = val * 0.264172
        # Liters to fluid ounces
        elif final == "lit floz":
            calc = val * 33.814
        # Liters to cups
        elif final == "lit cup":
            calc = val * 4.22675


        if calc != "":
            con1 = valid[categoryTo][validFrom][0]
            con2 = valid[categoryTo][validTo][0]
            msg = ("> {val} {con1} is equal to {calc} {con2}.").format(val=val, calc=calc, con1=con1, con2=con2)
        else:
            msg = "Invalid set of conversions."

        return await ctx.send(f"{msg}")



    @commands.group(aliases=["converter"])
    async def conv(self, ctx: commands.Context):
        """Some utility converters."""

  
    

    @conv.group(aliases=['fluidounce', 'fluidoz', 'fluidounces'])
    async def floz(self, ctx: commands.Context):
        """
        Fluid ounces to liters, gallons, and cups

        Usage:
        `[p]conv floz lit` Fluid ounces to liters
        `[p]conv floz gal` Fluid ounces to gallons
        `[p]conv floz cup` Fluid ounces to cups
        """
    
    @floz.command(name="lit", aliases=['liters', 'liter', 'li'])
    async def floz_to_lit(self, ctx: commands.Context, val: float):
        """Fluid ounces to liters."""
        output = val / 33.814
        await ctx.send(_("> {val:,} fluid ounces is equal to {output:,} liters.").format(val=val, output=output))

    @floz.command(name="gal", aliases=['gallon', 'gallons', 'gals'])
    async def floz_to_gal(self, ctx: commands.Context, val: float):
        """Fluid ounces to gallons."""
        output = val / 128
        await ctx.send(_("> {val:,} fluid ounces is equal to {output:,} gallons.").format(val=val, output=output))

    @floz.command(name="cup", aliases=['cups'])
    async def floz_to_cup(self, ctx: commands.Context, val: float):
        """Fluid ounces to cups."""
        output = val / 8
        await ctx.send(_("> {val:,} fluid ounces is equal to {output:,} cups.").format(val=val, output=output))


    @conv.group(aliases=['cups'])
    async def cup(self, ctx: commands.Context):
        """
        Cups to liters, gallons, and fluid ounces

        Usage:
        `[p]conv cup lit` Cups to liters
        `[p]conv cup gal` Cups to gallons
        `[p]conv cup oz` Cups to fluid ounces
        """
    
    @cup.command(name="lit", aliases=['liters', 'liter', 'li'])
    async def cup_to_lit(self, ctx: commands.Context, val: float):
        """Cups to liters."""
        output = val * 0.236588
        await ctx.send(_("> {val:,} cups is equal to {output:,} liters.").format(val=val, output=output))

    @cup.command(name="gal", aliases=['gallon', 'gallons', 'gals'])
    async def cup_to_gal(self, ctx: commands.Context, val: float):
        """Cups to gallons."""
        output = val * 0.0625
        await ctx.send(_("> {val:,} cups is equal to {output:,} gallons.").format(val=val, output=output))

    @cup.command(name="oz", aliases=['floz', 'fluidounces', 'fluidounce'])
    async def cup_to_floz(self, ctx: commands.Context, val: float):
        """Cups to fluid ounces."""
        output = val * 8
        await ctx.send(_("> {val:,} cups is equal to {output:,} fluid ounces.").format(val=val, output=output))


    @conv.command()
    async def mi(self, ctx: commands.Context, val: float):
        """Miles to kilometers."""
        output = round((val * 1.609344), 1)
        await ctx.send(_("> {val:,} miles is equal to {output:,} kilometers.").format(val=val, output=output))

    @conv.command()
    async def km(self, ctx: commands.Context, val: float):
        """Kilometers to miles."""
        output = round((val / 1.609344), 1)
        await ctx.send(_("> {val:,} kilometers is equal to {output:,} miles.").format(val=val, output=output))


    @conv.command()
    async def todate(self, ctx: commands.Context, timestamp: Union[int, float]):
        """Convert a unix timestamp to a readable datetime."""
        try:
            convert = datetime.fromtimestamp(int(timestamp), timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            g = datetime.fromtimestamp(int(timestamp))
            curr = datetime.fromtimestamp(int(datetime.now().timestamp()))
            secs = str((curr - g).total_seconds())
            seconds = secs[1:][:-2] if "-" in secs else secs[:-2] if ".0" in secs else secs
            delta = humanize_timedelta(seconds=int(seconds))
            when = (
                _("It will be in {}.").format(delta)
                if g > curr
                else _("It was {} ago.").format(delta)
            )
            await ctx.send(
                _("Successfully converted `{timestamp}` to `{convert}`\n{when}").format(
                    timestamp=int(timestamp), convert=convert, when=when
                )
            )
        except (ValueError, OverflowError, OSError):
            return await ctx.send(_("`{}` is not a valid timestamp.").format(timestamp))

    @conv.command()
    async def tounix(self, ctx: commands.Context, *, date: str):
        """
        Convert a date to a unix timestamp.

        Note: Need to respect this pattern `%Y-%m-%d %H:%M:%S`.
        Year-month-day Hour:minute:second
        Minimum to work is Year.
        """
        patterns = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H",
            "%Y-%m-%d",
            "%Y-%m",
            "%Y",
            "%m",
            "%d",
        ]
        for pattern in patterns:
            with contextlib.suppress(ValueError):
                convert = int(datetime.strptime(date, pattern).timestamp())
        try:
            given = datetime.fromtimestamp(int(convert))
        except UnboundLocalError:
            return await ctx.send(_("`{}` is not a valid timestamp.").format(date))
        curr = datetime.fromtimestamp(int(datetime.now().timestamp()))
        secs = str((curr - given).total_seconds())
        seconds = secs[1:][:-2] if "-" in secs else secs[:-2] if ".0" in secs else secs
        delta = humanize_timedelta(seconds=int(seconds))
        when = (
            _("It will be in {}.").format(delta)
            if given > curr
            else _("It was {} ago.").format(delta)
        )

        await ctx.send(
            _("Successfully converted `{date}` to `{convert}`\n{when}").format(
                date=date, convert=convert, when=when
            )
        )
