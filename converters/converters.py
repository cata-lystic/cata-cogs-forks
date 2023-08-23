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

        # Check if convertTo is a digit/int/float
        # If it is, use converTo as the val
        # This is because c, f, mi, and km don't require a convertTo
        try:
            float(convertTo)
            return await ctx.send("convertTo is a number")
        except ValueError:
            return await ctx.send("converTo is NOT a number")

        if (convertFrom == convertTo):
            return await ctx.send("You can't convert the same unit")

        # List of valid conversions
        valid = {
            'lb': ['pounds', 'lb', 'lbs', 'pound'],
            'kg': ['kilograms', 'kg', 'ki', 'kgs', 'kilo', 'kilos', 'kilogram'],
            'oz': ['ounces', 'oz' 'ounce', 'os'],
            'gr': ['grams', 'gr', 'gram'],
            'ton': ['tons', 'ton', 'uston'],
            'tonne': ['tonnes', 'tonne', 'ukton'],
            'c': ['Celsius', 'c', 'celsius'],
            'f': ['Fahrenheit', 'f', 'fahrenheit']
        }

        # Check to make sure chosen conversions are valid
        key_list = list(valid.keys())
        val_list = list(valid.values())

        # Loop through each list in the dictionary and see if it exists.
        # if it does, return the index

        validFrom = "Invalid convertFrom"
        validTo = "Invalid convertTo"

        for i in range(len(val_list)):
            if convertFrom in val_list[i]:
                validFrom = key_list[i]

            if convertTo in val_list[i]:
                validTo = key_list[i]
        
        if validFrom != "Invalid convertFrom" and validTo != "Invalid convertTo":
            final = f"{validFrom} {validTo}"
        else:
            return await ctx.send(f"{validFrom} | {validTo} | {val}")

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
        elif final == "c":
            calc = round((val * 1.8) + 32, 1)
        # Fahrenheit to Celsius
        elif final == "f":
            calc = round((val - 32) / 1.8, 1)
        

        if calc != "":
            con1 = valid[validFrom][0]
            con2 = valid[validTo][0]
            msg = ("> {val} {con1} is equal to {calc} {con2}.").format(val=val, calc=calc, con1=con1, con2=con2)
        else:
            msg = "Invalid set of conversions."

        return await ctx.send(f"{msg}")



    @commands.group(aliases=["converter"])
    async def conv(self, ctx: commands.Context):
        """Some utility converters."""

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


    @conv.group(aliases=['feet', 'foot'])
    async def ft(self, ctx: commands.Context):
        """
        Feet to meters, centimeters, or inches.

        Usage:
        `[p]conv ft me` Feet to meters
        `[p]conv ft cm` Feet to centimeters
        `[p]conv ft in` Feet to inches
        """

    @ft.command(name="me", aliases=['meters', 'meter', 'm'])
    async def ft_to_me(self, ctx: commands.Context, val: float):
        """Feet to meters."""
        output = val * 0.3048
        await ctx.send(_("> {val:,} feet is equal to {output:,} meters.").format(val=val, output=output))
    
    @ft.command(name="cm", aliases=['c', 'centimeter', 'centimeters'])
    async def ft_to_cm(self, ctx: commands.Context, val: float):
        """Feet to centimeters."""
        output = val * 30.48
        await ctx.send(_("> {val:,} feet is equal to {output:,} centimeters.").format(val=val, output=output))

    @ft.command(name="in", aliases=['inches', 'inch', 'i'])
    async def ft_to_in(self, ctx: commands.Context, val: float):
        """Feet to inches."""
        output = val * 12
        await ctx.send(_("> {val:,} feet is equal to {output:,} inches.").format(val=val, output=output))


    @conv.group(aliases=['meters', 'meter', 'm'])
    async def me(self, ctx: commands.Context):
        """
        Meters to centimeters, feet, and inches.

        Usage:
        `[p]conv me cm` Meters to centimeters
        `[p]conv me ft` Meters to feet
        `[p]conv me in` Meters to inches
        """

    @me.command(name="cm", aliases=['c', 'centimeter', 'centimeters'])
    async def me_to_cm(self, ctx: commands.Context, val: float):
        """Meters to centimeters."""
        output = val * 100
        await ctx.send(_("> {val:,} meters is equal to {output:,} centimeters.").format(val=val, output=output))

    @me.command(name="ft", aliases=['feet', 'foot', 'f'])
    async def me_to_ft(self, ctx: commands.Context, val: float):
        """Meters to feet."""
        output = val * 3.28084
        await ctx.send(_("> {val:,} meters is equal to {output:,} feet.").format(val=val, output=output))

    @me.command(name="in", aliases=['inches', 'inch', 'i'])
    async def me_to_in(self, ctx: commands.Context, val: float):
        """Meters to inches."""
        output = val * 39.37
        await ctx.send(_("> {val:,} meters is equal to {output:,} inches.").format(val=val, output=output))


    @conv.group(aliases=['centimeters', 'centimeter'])
    async def cm(self, ctx: commands.Context):
        """
        Centimeters to meters, feet, and inches.

        Usage:
        `[p]conv cm me` Centimeters to meters
        `[p]conv cm ft` Centimeters to feet
        `[p]conv cm in` Centimeters to inches
        """

    @cm.command(name="me", aliases=['meters', 'meter', 'm'])
    async def cm_to_m(self, ctx: commands.Context, val: float):
        """Centimeters to meters."""
        output = val / 100
        await ctx.send(_("> {val:,} centimeters is equal to {output:,} meters.").format(val=val, output=output))
    
    @cm.command(name="ft", aliases=['f', 'feet', 'foot'])
    async def cm_to_ft(self, ctx: commands.Context, val: float):
        """Centimeters to feet."""
        output = val / 30.48
        await ctx.send(_("> {val:,} centimeters is equal to {output:,} feet.").format(val=val, output=output))

    @cm.command(name="in", aliases=['inches', 'inch', 'i'])
    async def cm_to_in(self, ctx: commands.Context, val: float):
        """Centimeters to inches."""
        output = val / 2.54
        await ctx.send(_("> {val:,} centimeters is equal to {output:,} inches.").format(val=val, output=output))
    

    @conv.group(aliases=['inches', 'in', 'i'])
    async def inch(self, ctx: commands.Context):
        """
        Inches to meters, centimeters, and feet.

        Usage:
        `[p]conv in ft` Inches to feet
        `[p]conv in me` Inches to meters
        `[p]conv in cm` Inches to centimeters
        """
    
    @inch.command(name="ft", aliases=['f', 'feet', 'foot'])
    async def in_to_ft(self, ctx: commands.Context, val: float):
        """Inches to feet."""
        output = val / 12
        await ctx.send(_("> {val:,} inches is equal to {output:,} feet.").format(val=val, output=output))

    @inch.command(name="me", aliases=['meter', 'meters', 'm'])
    async def in_to_m(self, ctx: commands.Context, val: float):
        """Inches to meters."""
        output = val * 0.0254
        await ctx.send(_("> {val:,} inches is equal to {output:,} meters.").format(val=val, output=output))

    @inch.command(name="cm", aliases=['c', 'centimeters'])
    async def in_to_cm(self, ctx: commands.Context, val: float):
        """Inches to centimeters."""
        output = val * 2.54
        await ctx.send(_("> {val:,} inches is equal to {output:,} centimeters.").format(val=val, output=output))


    @conv.group(aliases=['gallon', 'gallons'])
    async def gal(self, ctx: commands.Context):
        """
        Gallons to liters, fluid ounces, and cups

        Usage:
        `[p]conv gal lit` Gallons to liters
        `[p]conv gal oz` Gallons to fluid ounces
        `[p]conv gal cup` Gallons to cups
        """
    
    @gal.command(name="lit", aliases=['liters', 'liter', 'li'])
    async def gal_to_lit(self, ctx: commands.Context, val: float):
        """Gallons to liters."""
        output = val * 3.78541
        await ctx.send(_("> {val:,} gallons is equal to {output:,} liters.").format(val=val, output=output))

    @gal.command(name="oz", aliases=['floz', 'ounce', 'fluidounce'])
    async def gal_to_oz(self, ctx: commands.Context, val: float):
        """Gallons to fluid ounces."""
        output = val * 128
        await ctx.send(_("> {val:,} gallons is equal to {output:,} fluid ounces.").format(val=val, output=output))

    @gal.command(name="cup", aliases=['cups'])
    async def gal_to_cup(self, ctx: commands.Context, val: float):
        """Gallons to cups."""
        output = val * 16
        await ctx.send(_("> {val:,} gallons is equal to {output:,} cups.").format(val=val, output=output))


    @conv.group(aliases=['liter', 'liters'])
    async def lit(self, ctx: commands.Context):
        """
        Liters to gallons, fluid ounces, and cups

        Usage:
        `[p]conv lit gal` Liters to gallons
        `[p]conv lit oz` Liters to fluid ounces
        `[p]conv lit cup` Liters to cups
        """
    
    @lit.command(name="gal", aliases=['gals', 'gallons', 'gallon'])
    async def lit_to_gal(self, ctx: commands.Context, val: float):
        """Liters to gallons."""
        output = val * 0.264172
        await ctx.send(_("> {val:,} liters is equal to {output:,} gallons.").format(val=val, output=output))

    @lit.command(name="oz", aliases=['floz', 'ounce', 'fluidounce'])
    async def lit_to_oz(self, ctx: commands.Context, val: float):
        """Liters to fluid ounces."""
        output = val * 33.814
        await ctx.send(_("> {val:,} liters is equal to {output:,} fluid ounces.").format(val=val, output=output))

    @lit.command(name="cup", aliases=['cups'])
    async def lit_to_cup(self, ctx: commands.Context, val: float):
        """Liters to cups."""
        output = val * 4.22675
        await ctx.send(_("> {val:,} liters is equal to {output:,} cups.").format(val=val, output=output))
    

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
