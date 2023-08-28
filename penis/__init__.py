from redbot.core.bot import Red
from .penis import Penis

async def setup(bot: Red):
    cog = Penis(bot)
    await bot.add_cog(cog)