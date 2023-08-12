# -*- coding: utf-8 -*-

'''
Validador da cog de admin.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext import commands

from discpybotframe.validation.validation_checks import ValidationChecks

if TYPE_CHECKING:
    from discpybotframe.discord.bot import Bot


class AdminCogValidator():

    '''
    Valida os comandos da cog de admin.
    '''

    @staticmethod
    async def shutdown_validation(ctx: commands.Context, bot: Bot, error: str, footer: str):
        '''
        Valida o comando de desligar o bot.
        '''

        return await ValidationChecks.require_adm(ctx, bot, error, footer)
