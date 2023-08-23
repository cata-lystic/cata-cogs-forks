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

    @conv.group(aliases=["c"])
    async def celsius(self, ctx: commands.Context):
        """
        Convert degree Celsius to Fahrenheit or Kelvin.
        See correct usage bellow.

        Usage:
        To Fahrenheit: `[p]conv celsius fahrenheit`
        To Kelvin: `[p]conv celsius kelvin`
        (You can also use `[p]conv c f` or `[p]conv c k`)
        """

    @celsius.command(name="fahrenheit", aliases=["f"])
    async def celsius_to_fahrenheit(self, ctx: commands.Context, temperature: float):
        """Convert degree Celsius to Fahrenheit."""
        fahrenheit = round((temperature * 1.8) + 32, 1)
        msg = _("{temp:,}° Celsius is equal to {f:,}° Fahrenheit.").format(
            temp=temperature, f=fahrenheit
        )
        await ctx.send(msg)

    @celsius.command(name="kelvin", aliases=["k"])
    async def celsius_to_kelvin(self, ctx: commands.Context, temperature: float):
        """Convert degree Celsius to Kelvin."""
        kelvin = round(temperature + 273.15, 1)
        msg = _("{temp:,}° Celsius is equal to {k:,}° Kelvin.").format(temp=temperature, k=kelvin)
        await ctx.send(msg)

    @conv.group(aliases=["f"])
    async def fahrenheit(self, ctx: commands.Context):
        """
        Convert Fahrenheit degree to Celsius or Kelvin.
        See correct usage bellow.

        Usage:
        To Celsius: `[p]conv fahrenheit celsius`
        To Kelvin: `[p]conv fahrenheit kelvin`
        (You can also use `[p]conv f c` or `[p]conv f k`)
        """

    @fahrenheit.command(name="celsius", aliases=["c"])
    async def fahrenheit_to_celsius(self, ctx: commands.Context, temperature: float):
        """Convert Fahrenheit degree to Celsius."""
        celsius = round((temperature - 32) / 1.8, 1)
        msg = _("{temp:,}° Fahrenheit is equal to {c:,}° Celsius.").format(
            temp=temperature, c=celsius
        )
        await ctx.send(msg)

    @fahrenheit.command(name="kelvin", aliases=["k"])
    async def fahrenheit_to_kelvin(self, ctx: commands.Context, temperature: float):
        """Convert Fahrenheit degree to Kelvin."""
        kelvin = round((temperature - 32) * (5 / 9) + 273.15, 1)
        msg = _("{temp:,}° Fahrenheit is equal to {k:,}° Kelvin.").format(
            temp=temperature, k=kelvin
        )
        await ctx.send(msg)

    @conv.group(aliases=["k"])
    async def kelvin(self, ctx: commands.Context):
        """
        Convert Kelvin degree to Celsius or Fahrenheit.
        See correct usage bellow.

        Usage:
        To Celsius: `[p]conv kelvin celsius`
        To Fahrenheit: `[p]conv kelvin fahrenheit`
        (You can also use `[p]conv f c` or `[p]conv f k`)
        """

    @kelvin.command(name="celsius", aliases=["c"])
    async def kelvin_to_celsius(self, ctx: commands.Context, temperature: float):
        """Convert Kelvin degree to Celsius."""
        celsius = round(temperature - 273.15, 1)
        msg = _("{temp:,}° Kelvin is equal to {c:,}° Celsius.").format(temp=temperature, c=celsius)
        await ctx.send(msg)

    @kelvin.command(name="fahrenheit", aliases=["f"])
    async def kelvin_to_fahrenheit(self, ctx: commands.Context, temperature: float):
        """Convert Kelvin degree to Fahrenheit."""
        fahrenheit = round((temperature - 273.15) * (9 / 5) + 32, 1)
        msg = _("{temp:,}° Kelvin is equal to {f:,}° Fahrenheit.").format(
            temp=temperature, f=fahrenheit
        )
        await ctx.send(msg)

    @conv.group()
    async def lb(self, ctx: commands.Context):
        """
        Convert pounds to kilograms.
        See correct usage bellow.

        Usage:
        `[p]conv lb kg`
        """

    @lb.group(name="kg")
    async def lb_to_kg(self, ctx: commands.Context, mass: float):
        """Convert pounds to kilograms."""
        kg = round((mass * 0.45359237), 1)
        await ctx.send(_("{mass:,} lb is equal to {kg:,} kg.").format(mass=mass, kg=kg))

    @conv.group()
    async def kg(self, ctx: commands.Context):
        """
        Convert kilograms to pounds.

        Usage:
        `[p]conv kg lb`
        """

    @kg.command(name="lb")
    async def kg_to_pounds(self, ctx: commands.Context, mass: float):
        """Convert kilograms to pounds."""
        lb = round((mass / 0.45359237), 1)
        await ctx.send(_("{mass:,} kg is equal to {lb:,} lb.").format(mass=mass, lb=lb))

    
    # Feet to meters, centimeters, inches by Cata-lystic
    @conv.group(aliases=['feet', 'foot'])
    async def ft(self, ctx: commands.Context):
        """
        Convert feet to meters, centimeters, or inches.

        Usage:
        `[p]conv ft me` Feet to meters
        `[p]conv ft cm` Feet to centimeters
        `[p]conv ft in` Feet to inches
        """

    @ft.command(name="me", aliases=['meters', 'meter', 'm'])
    async def ft_to_me(self, ctx: commands.Context, length: float):
        """Convert feet to meters."""
        m = length * 0.3048
        await ctx.send(_("{length:,} feet is equal to {m:,} meters.").format(length=length, m=m))
    
    @ft.command(name="cm", aliases=['c', 'centimeter', 'centimeters'])
    async def ft_to_cm(self, ctx: commands.Context, length: float):
        """Convert feet to centimeters."""
        cm = length * 30.48
        await ctx.send(_("{length:,} feet is equal to {cm:,} centimeters.").format(length=length, cm=cm))

    @ft.command(name="in", aliases=['inches', 'inch', 'i'])
    async def ft_to_in(self, ctx: commands.Context, length: float):
        """Convert feet to inches."""
        i = length * 12
        await ctx.send(_("{length:,} feet is equal to {i:,} inches.").format(length=length, i=i))

    # Meters to centimeters, feet, inches by Cata-lystic
    @conv.group(aliases=['meters', 'meter', 'm'])
    async def me(self, ctx: commands.Context):
        """
        Convert meters to centimeters, feet, or inches.

        Usage:
        `[p]conv me cm` Meters to centimeters
        `[p]conv me ft` Meters to feet
        `[p]conv me in` Meters to inches
        """

    @me.command(name="cm", aliases=['c', 'centimeter', 'centimeters'])
    async def me_to_cm(self, ctx: commands.Context, length: float):
        """Convert meters to centimeters."""
        cm = length * 100
        await ctx.send(_("{length:,} meters is equal to {cm:,} centimeters.").format(length=length, cm=cm))

    @me.command(name="ft", aliases=['feet', 'foot', 'f'])
    async def me_to_ft(self, ctx: commands.Context, length: float):
        """Convert meters to feet."""
        ft = length * 3.28084
        await ctx.send(_("{length:,} meters is equal to {ft:,} feet.").format(length=length, ft=ft))

    @me.command(name="in", aliases=['inches', 'inch', 'i'])
    async def me_to_in(self, ctx: commands.Context, length: float):
        """Convert meters to inches."""
        i = length * 39.37
        await ctx.send(_("{length:,} meters is equal to {i:,} inches.").format(length=length, i=i))

    # Centimeters to meters, feet, inches by Cata-lystic
    @conv.group(aliases=['centimeters', 'centimeter'])
    async def cm(self, ctx: commands.Context):
        """
        Convert feet to meters, centimeters, or inches.

        Usage:
        `[p]conv cm me` Centimeters to meters
        `[p]conv cm ft` Centimeters to feet
        `[p]conv cm in` Centimeters to inches
        """

    @cm.command(name="me", aliases=['meters', 'meter', 'm'])
    async def cm_to_m(self, ctx: commands.Context, length: float):
        """Convert centimeters to meters."""
        m = length / 100
        await ctx.send(_("{length:,} centimeters is equal to {m:,} meters.").format(length=length, m=m))
    
    @cm.command(name="ft", aliases=['f', 'feet', 'foot'])
    async def cm_to_ft(self, ctx: commands.Context, length: float):
        """Convert centimeters to feet."""
        ft = length / 30.48
        await ctx.send(_("{length:,} centimeters is equal to {ft:,} feet.").format(length=length, ft=ft))

    @cm.command(name="in", aliases=['inches', 'inch', 'i'])
    async def cm_to_in(self, ctx: commands.Context, length: float):
        """Convert centimeters to inches."""
        i = length / 2.54
        await ctx.send(_("{length:,} centimeters is equal to {i:,} inches.").format(length=length, i=i))
    
    # Inches to centimeters, meters, feet by Cata-lystic
    @conv.group(aliases=['inches', 'in', 'i'])
    async def inch(self, ctx: commands.Context):
        """
        Convert inches to meters, centimeters, or feet.

        Usage:
        `[p]conv in ft` Inches to feet
        `[p]conv in me` Inches to meters
        `[p]conv in cm` Inches to centimeters
        """
    
    @inch.command(name="ft", aliases=['f', 'feet', 'foot'])
    async def in_to_ft(self, ctx: commands.Context, length: float):
        """Convert inches to feet."""
        ft = length / 12
        await ctx.send(_("{length:,} inches is equal to {ft:,} feet.").format(length=length, ft=ft))

    @inch.command(name="me", aliases=['meter', 'meters', 'm'])
    async def in_to_m(self, ctx: commands.Context, length: float):
        """Convert inches to meters."""
        m = length * 0.0254
        await ctx.send(_("{length:,} inches is equal to {m:,} meters.").format(length=length, m=m))

    @inch.command(name="cm", aliases=['c', 'centimeters'])
    async def in_to_cm(self, ctx: commands.Context, length: float):
        """Convert inches to centimeters."""
        cm = length * 2.54
        await ctx.send(_("{length:,} inches is equal to {cm:,} centimeters.").format(length=length, cm=cm))
    

    @conv.group()
    async def mi(self, ctx: commands.Context):
        """
        Convert miles to kilometers.
        See correct usage bellow.

        Usage:
        `[p]conv mi km`
        """

    @mi.command(name="km")
    async def mi_to_km(self, ctx: commands.Context, length: float):
        """Convert miles to kilometers."""
        km = round((length * 1.609344), 1)
        await ctx.send(_("{length:,} mi is equal to {km:,} km.").format(length=length, km=km))

    @conv.group()
    async def km(self, ctx: commands.Context):
        """
        Convert kilometers to miles.
        See correct usage bellow.

        Usage:
        `[p]conv km mi`
        """

    @km.command(name="mi")
    async def km_to_mi(self, ctx: commands.Context, length: float):
        """Convert kilometers to miles."""
        mi = round((length / 1.609344), 1)
        await ctx.send(_("{length:,} km is equal to {mi:,} mi.").format(length=length, mi=mi))
