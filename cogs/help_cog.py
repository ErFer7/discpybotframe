# -*- coding:utf-8 -*-

'''
Módulo para a cog dos comandos de ajuda
'''

from discord.ext import commands

from discpybotframe.utils.utilities import DiscordUtilities
from discpybotframe.cogs.cog import Cog


class HelpCog(Cog):

    '''
    Cog dos comandos de ajuda.
    '''

    _help_text: str

    # Construtor
    def __init__(self, bot, help_text) -> None:
        super().__init__(bot)
        self._help_text = help_text
        self.bot.log("HelpCog", "Help system initialized")

    # Comandos
    @commands.command(name="help", aliases=("ajuda", "h", "aj"))
    async def custom_help(self, ctx) -> None:
        '''
        Envia uma mensagem de ajuda.
        '''

        self.bot.log("HelpCog", f"<help> (Author: {ctx.author.name})")
        await DiscordUtilities.send_message(ctx, "Ajuda", self._help_text, "help")
