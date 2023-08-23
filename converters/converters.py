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

    @conv.command(aliases=["celsius"])
    async def c(self, ctx: commands.Context, val: float):
        """Celsius to Fahrenheit."""
        output = round((val * 1.8) + 32, 1)
        msg = _("> {val:,}° Celsius is equal to {output:,}° Fahrenheit.").format(
            val=val, output=output
        )
        await ctx.send(msg)

    @conv.command(aliases=["fahrenheit"])
    async def f(self, ctx: commands.Context, val: float):
        """Fahrenheit to Celsius."""
        output = round((val - 32) / 1.8, 1)
        msg = _("> {val:,}° Fahrenheit is equal to {output:,}° Celsius.").format(
            val=val, output=output
        )
        await ctx.send(msg)

    @conv.group(aliases=['pound', 'pounds'])
    async def lb(self, ctx: commands.Context):
        """
        Pounds to kilograms, ounces, and grams.

        Usage:
        `[p]conv lb kg` Pounds to kilograms
        `[p]conv lb oz` Pounds to ounces
        `[p]conv lb g` Pounds to grams
        """

    @lb.command(name="kg")
    async def lb_to_kg(self, ctx: commands.Context, val: float):
        """Pounds to kilograms."""
        output = round((val * 0.45359237), 1)
        await ctx.send(_("{val:,} pounds is equal to {output:,} kilograms.").format(val=val, output=output))

    @lb.command(name="oz", aliases=['ounce', 'ounces'])
    async def lb_to_oz(self, ctx: commands.Context, val: float):
        """Pounds to ounces."""
        output = val * 16
        await ctx.send(_("{val:,} pounds is equal to {output:,} ounces.").format(val=val, output=output))

    @lb.command(name="g", aliases=['gr', 'gram', 'grams'])
    async def lb_to_g(self, ctx: commands.Context, val: float):
        """Pounds to grams."""
        output = val * 453.592
        await ctx.send(_("{val:,} pounds is equal to {output:,} grams.").format(val=val, output=output))

    @conv.group(aliases=['kilograms', 'kilogram', 'kilo'])
    async def kg(self, ctx: commands.Context):
        """
        Kilograms to pounds, ounces, and grams

        Usage:
        `[p]conv kg lb`
        `[p]conv kg oz`
        `[p]conv kg g`
        """

    @kg.command(name="lb")
    async def kg_to_pounds(self, ctx: commands.Context, val: float):
        """Kilograms to pounds."""
        output = round((val / 0.45359237), 1)
        await ctx.send(_("{val:,} kilograms is equal to {output:,} pounds.").format(val=val, output=output))

    @kg.command(name="oz", aliases=['ounce', 'ounces'])
    async def kg_to_oz(self, ctx: commands.Context, val: float):
        """Kilograms to ounces."""
        output = val * 35.2739619
        await ctx.send(_("{val:,} kilograms is equal to {output:,} ounces.").format(val=val, output=output))

    @kg.command(name="g", aliases=['gr', 'gram', 'grams'])
    async def kg_to_g(self, ctx: commands.Context, val: float):
        """Kilograms to grams."""
        output = val * 1000
        await ctx.send(_("{val:,} kilograms is equal to {output:,} grams.").format(val=val, output=output))


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
        await ctx.send(_("{val:,} feet is equal to {output:,} meters.").format(val=val, output=output))
    
    @ft.command(name="cm", aliases=['c', 'centimeter', 'centimeters'])
    async def ft_to_cm(self, ctx: commands.Context, val: float):
        """Feet to centimeters."""
        output = val * 30.48
        await ctx.send(_("{val:,} feet is equal to {output:,} centimeters.").format(val=val, output=output))

    @ft.command(name="in", aliases=['inches', 'inch', 'i'])
    async def ft_to_in(self, ctx: commands.Context, val: float):
        """Feet to inches."""
        output = val * 12
        await ctx.send(_("{val:,} feet is equal to {output:,} inches.").format(val=val, output=output))


    @conv.group(aliases=['meters', 'meter', 'm'])
    async def me(self, ctx: commands.Context):
        """
        Meters to centimeters, feet, or inches.

        Usage:
        `[p]conv me cm` Meters to centimeters
        `[p]conv me ft` Meters to feet
        `[p]conv me in` Meters to inches
        """

    @me.command(name="cm", aliases=['c', 'centimeter', 'centimeters'])
    async def me_to_cm(self, ctx: commands.Context, val: float):
        """Meters to centimeters."""
        output = val * 100
        await ctx.send(_("{val:,} meters is equal to {output:,} centimeters.").format(val=val, output=output))

    @me.command(name="ft", aliases=['feet', 'foot', 'f'])
    async def me_to_ft(self, ctx: commands.Context, val: float):
        """Meters to feet."""
        output = val * 3.28084
        await ctx.send(_("{val:,} meters is equal to {output:,} feet.").format(val=val, output=output))

    @me.command(name="in", aliases=['inches', 'inch', 'i'])
    async def me_to_in(self, ctx: commands.Context, val: float):
        """Meters to inches."""
        output = val * 39.37
        await ctx.send(_("{val:,} meters is equal to {output:,} inches.").format(val=val, output=output))


    @conv.group(aliases=['centimeters', 'centimeter'])
    async def cm(self, ctx: commands.Context):
        """
        Centimeters to meters, feet, or inches.

        Usage:
        `[p]conv cm me` Centimeters to meters
        `[p]conv cm ft` Centimeters to feet
        `[p]conv cm in` Centimeters to inches
        """

    @cm.command(name="me", aliases=['meters', 'meter', 'm'])
    async def cm_to_m(self, ctx: commands.Context, val: float):
        """Centimeters to meters."""
        output = val / 100
        await ctx.send(_("{val:,} centimeters is equal to {output:,} meters.").format(val=val, output=output))
    
    @cm.command(name="ft", aliases=['f', 'feet', 'foot'])
    async def cm_to_ft(self, ctx: commands.Context, val: float):
        """Centimeters to feet."""
        output = val / 30.48
        await ctx.send(_("{val:,} centimeters is equal to {output:,} feet.").format(val=val, output=output))

    @cm.command(name="in", aliases=['inches', 'inch', 'i'])
    async def cm_to_in(self, ctx: commands.Context, val: float):
        """Centimeters to inches."""
        output = val / 2.54
        await ctx.send(_("{val:,} centimeters is equal to {output:,} inches.").format(val=val, output=output))
    

    @conv.group(aliases=['inches', 'in', 'i'])
    async def inch(self, ctx: commands.Context):
        """
        Inches to meters, centimeters, or feet.

        Usage:
        `[p]conv in ft` Inches to feet
        `[p]conv in me` Inches to meters
        `[p]conv in cm` Inches to centimeters
        """
    
    @inch.command(name="ft", aliases=['f', 'feet', 'foot'])
    async def in_to_ft(self, ctx: commands.Context, val: float):
        """Inches to feet."""
        output = val / 12
        await ctx.send(_("{val:,} inches is equal to {output:,} feet.").format(val=val, output=output))

    @inch.command(name="me", aliases=['meter', 'meters', 'm'])
    async def in_to_m(self, ctx: commands.Context, val: float):
        """Inches to meters."""
        output = val * 0.0254
        await ctx.send(_("{val:,} inches is equal to {output:,} meters.").format(val=val, output=output))

    @inch.command(name="cm", aliases=['c', 'centimeters'])
    async def in_to_cm(self, ctx: commands.Context, val: float):
        """Inches to centimeters."""
        output = val * 2.54
        await ctx.send(_("{val:,} inches is equal to {output:,} centimeters.").format(val=val, output=output))


    @conv.group(aliases=['gallon', 'gallons'])
    async def gal(self, ctx: commands.Context):
        """
        Inches to meters, centimeters, or feet.

        Usage:
        `[p]conv gal lit` Gallons to liters
        `[p]conv gal cup` Gallons to cups
        `[p]conv gal oz` Gallons to fluid ounces
        """
    
    @inch.command(name="lit", aliases=['liters', 'liter', 'li'])
    async def gal_to_lit(self, ctx: commands.Context, val: float):
        """Gallons to liters."""
        output = val * 3.78541
        await ctx.send(_("{val:,} gallons is equal to {output:,} liters.").format(val=val, output=output))

    @inch.command(name="oz", aliases=['floz', 'ounce', 'fluidounce'])
    async def gal_to_oz(self, ctx: commands.Context, val: float):
        """Gallons to fluid ounces."""
        output = val * 128
        await ctx.send(_("{val:,} gallons is equal to {output:,} fluid ounces.").format(val=val, output=output))

    @inch.command(name="cup", aliases=['cups'])
    async def gal_to_cup(self, ctx: commands.Context, val: float):
        """Gallons to cups."""
        output = val * 16
        await ctx.send(_("{val:,} gallons is equal to {output:,} cups.").format(val=val, output=output))
    

    @conv.command()
    async def mi(self, ctx: commands.Context, val: float):
        """Miles to kilometers."""
        output = round((val * 1.609344), 1)
        await ctx.send(_("{val:,} miles is equal to {output:,} kilometers.").format(val=val, output=output))

    @conv.command()
    async def km(self, ctx: commands.Context, val: float):
        """Kilometers to miles."""
        output = round((val / 1.609344), 1)
        await ctx.send(_("{val:,} kilometers is equal to {output:,} miles.").format(val=val, output=output))
