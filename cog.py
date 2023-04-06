# -*- coding: utf-8 -*-

'''
Módulo para a definição de uma cog.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from discpybotframe.bot import Bot


class Cog(commands.Cog):

    '''
    Definição base de cog.
    '''

    _bot: Bot

    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    @property
    def bot(self) -> Bot:
        '''
        Getter do bot.
        '''

        return self._bot
