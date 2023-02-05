# -*- coding:utf-8 -*-

'''
Módulo para a cog dos comandos de ajuda
'''

from datetime import datetime

from discord.ext import commands

from .utilities import DiscordUtilities


class HelpCog(commands.Cog):

    '''
    Cog dos comandos de ajuda.
    '''

    _help_text: str

    # Construtor
    def __init__(self, help_text) -> None:

        self._help_text = help_text

        print(f"[{datetime.now()}][Help]: Help system initialized")

    # Comandos
    @commands.command(name="help", aliases=("ajuda", "h", "aj"))
    async def custom_help(self, ctx) -> None:
        '''
        Envia uma mensagem de ajuda.
        '''

        print(f"[{datetime.now()}][Help]: <help> (Author: {ctx.author.name})")
        await DiscordUtilities.send_message(ctx, "Ajuda", self._help_text, "help")
