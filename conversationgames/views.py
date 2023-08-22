import functools
from typing import Callable, Dict, List, Optional, Union

import discord
from redbot.core import commands

class CGView(discord.ui.View):
    def __init__(
        self,
        ctx: commands.Context,
        result: Dict[str, Union[str, Dict[str, str]]],
        timeout: float = 120.0,
    ) -> None:
        super().__init__(timeout=timeout)
        self._ctx: commands.Context = ctx
        self._result: Dict[str, Union[str, Dict[str, str]]] = result
        self._message: Optional[discord.Message] = None

    async def on_timeout(self) -> None:
        for item in self.children:
            item: discord.ui.Item
            item.disabled = True  # type: ignore
        try:
            await self._message.edit(view=self)  # type: ignore
        except discord.HTTPException:
            pass

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self._ctx.author.id != interaction.user.id:
            await interaction.response.send_message(
                "You are not allowed to use this interaction", ephemeral=True
            )
            return False
        return True

    @staticmethod
    async def _callback(interaction: discord.Interaction) -> None:  # type: ignore
        await interaction.response.defer()
        embed: discord.Embed = discord.Embed(
            description=self.view._result["question"] if self.values[0] == "English" else self.view._result["translations"][self.values[0]],  # type: ignore
            color=await self.view._ctx.embed_color(),  # type: ignore
        )
        embed.set_footer(
            text=f"Rating: {self.view._result['rating']} | ID: {self.view._result['id']}"  # type: ignore
        )
        await interaction.edit_original_response(embed=embed)
