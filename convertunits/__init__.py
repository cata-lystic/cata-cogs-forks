from redbot.core.bot import Red
from .convertunits import 

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)

async def setup(bot: Red):
    cog = Convertunits(bot)
    await bot.add_cog(cog)
