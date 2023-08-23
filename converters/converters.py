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

    @conv.group(aliases=["celsius"])
    async def c(self, ctx: commands.Context):
        """
        Celsius to Fahrenheit.

        Usage:
        `[p]conv c f`
        """

    @c.command(name="f", aliases=["fahrenheit"])
    async def celsius_to_fahrenheit(self, ctx: commands.Context, temperature: float):
        """Celsius to Fahrenheit."""
        fahrenheit = round((temperature * 1.8) + 32, 1)
        msg = _("{temp:,}° Celsius is equal to {f:,}° Fahrenheit.").format(
            temp=temperature, f=fahrenheit
        )
        await ctx.send(msg)

    @conv.group(aliases=["fahrenheit"])
    async def f(self, ctx: commands.Context):
        """
        Fahrenheit to Celsius.

        Usage:
        `[p]conv f c`
        """

    @f.command(name="celsius", aliases=["c"])
    async def fahrenheit_to_celsius(self, ctx: commands.Context, temperature: float):
        """Fahrenheit to Celsius."""
        celsius = round((temperature - 32) / 1.8, 1)
        msg = _("{temp:,}° Fahrenheit is equal to {c:,}° Celsius.").format(
            temp=temperature, c=celsius
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
    async def lb_to_kg(self, ctx: commands.Context, mass: float):
        """Pounds to kilograms."""
        kg = round((mass * 0.45359237), 1)
        await ctx.send(_("{mass:,} pounds is equal to {kg:,} kilograms.").format(mass=mass, kg=kg))

    @lb.command(name="oz", aliases=['ounce', 'ounces'])
    async def lb_to_oz(self, ctx: commands.Context, mass: float):
        """Pounds to ounces."""
        oz = mass * 16
        await ctx.send(_("{mass:,} pounds is equal to {oz:,} ounces.").format(mass=mass, oz=oz))

    @lb.command(name="g", aliases=['gr', 'gram', 'grams'])
    async def lb_to_g(self, ctx: commands.Context, mass: float):
        """Pounds to grams."""
        g = mass * 453.592
        await ctx.send(_("{mass:,} pounds is equal to {g:,} grams.").format(mass=mass, g=g))

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
    async def kg_to_pounds(self, ctx: commands.Context, mass: float):
        """Kilograms to pounds."""
        lb = round((mass / 0.45359237), 1)
        await ctx.send(_("{mass:,} kilograms is equal to {lb:,} pounds.").format(mass=mass, lb=lb))

    @kg.command(name="oz", aliases=['ounce', 'ounces'])
    async def kg_to_oz(self, ctx: commands.Context, mass: float):
        """Kilograms to ounces."""
        oz = mass * 35.2739619
        await ctx.send(_("{mass:,} kilograms is equal to {oz:,} ounces.").format(mass=mass, oz=oz))

    @kg.command(name="g", aliases=['gr', 'gram', 'grams'])
    async def kg_to_g(self, ctx: commands.Context, mass: float):
        """Kilograms to grams."""
        g = mass * 1000
        await ctx.send(_("{mass:,} kilograms is equal to {g:,} grams.").format(mass=mass, g=g))


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
    async def ft_to_me(self, ctx: commands.Context, length: float):
        """Feet to meters."""
        m = length * 0.3048
        await ctx.send(_("{length:,} feet is equal to {m:,} meters.").format(length=length, m=m))
    
    @ft.command(name="cm", aliases=['c', 'centimeter', 'centimeters'])
    async def ft_to_cm(self, ctx: commands.Context, length: float):
        """Feet to centimeters."""
        cm = length * 30.48
        await ctx.send(_("{length:,} feet is equal to {cm:,} centimeters.").format(length=length, cm=cm))

    @ft.command(name="in", aliases=['inches', 'inch', 'i'])
    async def ft_to_in(self, ctx: commands.Context, length: float):
        """Feet to inches."""
        i = length * 12
        await ctx.send(_("{length:,} feet is equal to {i:,} inches.").format(length=length, i=i))


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
    async def me_to_cm(self, ctx: commands.Context, length: float):
        """Meters to centimeters."""
        cm = length * 100
        await ctx.send(_("{length:,} meters is equal to {cm:,} centimeters.").format(length=length, cm=cm))

    @me.command(name="ft", aliases=['feet', 'foot', 'f'])
    async def me_to_ft(self, ctx: commands.Context, length: float):
        """Meters to feet."""
        ft = length * 3.28084
        await ctx.send(_("{length:,} meters is equal to {ft:,} feet.").format(length=length, ft=ft))

    @me.command(name="in", aliases=['inches', 'inch', 'i'])
    async def me_to_in(self, ctx: commands.Context, length: float):
        """Meters to inches."""
        i = length * 39.37
        await ctx.send(_("{length:,} meters is equal to {i:,} inches.").format(length=length, i=i))


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
    async def cm_to_m(self, ctx: commands.Context, length: float):
        """Centimeters to meters."""
        m = length / 100
        await ctx.send(_("{length:,} centimeters is equal to {m:,} meters.").format(length=length, m=m))
    
    @cm.command(name="ft", aliases=['f', 'feet', 'foot'])
    async def cm_to_ft(self, ctx: commands.Context, length: float):
        """Centimeters to feet."""
        ft = length / 30.48
        await ctx.send(_("{length:,} centimeters is equal to {ft:,} feet.").format(length=length, ft=ft))

    @cm.command(name="in", aliases=['inches', 'inch', 'i'])
    async def cm_to_in(self, ctx: commands.Context, length: float):
        """Centimeters to inches."""
        i = length / 2.54
        await ctx.send(_("{length:,} centimeters is equal to {i:,} inches.").format(length=length, i=i))
    

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
    async def in_to_ft(self, ctx: commands.Context, length: float):
        """Inches to feet."""
        ft = length / 12
        await ctx.send(_("{length:,} inches is equal to {ft:,} feet.").format(length=length, ft=ft))

    @inch.command(name="me", aliases=['meter', 'meters', 'm'])
    async def in_to_m(self, ctx: commands.Context, length: float):
        """Inches to meters."""
        m = length * 0.0254
        await ctx.send(_("{length:,} inches is equal to {m:,} meters.").format(length=length, m=m))

    @inch.command(name="cm", aliases=['c', 'centimeters'])
    async def in_to_cm(self, ctx: commands.Context, length: float):
        """Inches to centimeters."""
        cm = length * 2.54
        await ctx.send(_("{length:,} inches is equal to {cm:,} centimeters.").format(length=length, cm=cm))
    

    @conv.group()
    async def mi(self, ctx: commands.Context):
        """
        Miles to kilometers.
        See correct usage bellow.

        Usage:
        `[p]conv mi km`
        """

    @mi.command(name="km")
    async def mi_to_km(self, ctx: commands.Context, length: float):
        """Miles to kilometers."""
        km = round((length * 1.609344), 1)
        await ctx.send(_("{length:,} mi is equal to {km:,} km.").format(length=length, km=km))

    @conv.group()
    async def km(self, ctx: commands.Context):
        """
        Kilometers to miles.
        See correct usage bellow.

        Usage:
        `[p]conv km mi`
        """

    @km.command(name="mi")
    async def km_to_mi(self, ctx: commands.Context, length: float):
        """Kilometers to miles."""
        mi = round((length / 1.609344), 1)
        await ctx.send(_("{length:,} km is equal to {mi:,} mi.").format(length=length, mi=mi))
