# -*- coding: utf-8 -*-

'''
Módulo para a validação
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from enum import Enum

from discord.ext import commands

from discpybotframe.utils.utilities import DiscordUtilities

if TYPE_CHECKING:
    from discpybotframe.discord.bot import Bot


class ArgumentType(Enum):

    '''
    Enumerador para os tipos de argumentos.
    '''

    INTEGER = 0
    FLOAT = 1


class ValidationChecks():

    '''
    Classe para definição de requisitos de validação.
    '''

    @staticmethod
    async def require_adm(ctx: commands.Context, bot: Bot, error: str, footer: str) -> bool:
        '''
        Verifica se o usuário é o administrador do bot.
        '''

        if not bot.is_admin(ctx.author.id):
            await DiscordUtilities.send_error_message(ctx, error, footer)
            return False
        return True

    @staticmethod
    async def require_guild(ctx: commands.Context, error: str, footer: str) -> bool:
        '''
        Verifica se o comando foi executado em um servidor.
        '''

        if ctx.guild is None:
            await DiscordUtilities.send_error_message(ctx, error, footer)
            return False
        return True

    @staticmethod
    async def require_arg_length_range(ctx: commands.Context,
                                       length_range: tuple[int, int],
                                       args: tuple,
                                       error: str,
                                       footer: str) -> bool:
        '''
        Verifica se o número de argumentos está dentro do intervalo.
        '''

        if len(args) < length_range[0] or len(args) > length_range[1]:
            await DiscordUtilities.send_error_message(ctx, error, footer)
            return False
        return True

    @staticmethod
    async def require_arg_type(ctx: commands.Context, arg: str, type_: ArgumentType, error: str, footer: str) -> bool:
        '''
        Verifica se o tipo de argumento é o esperado.
        '''

        if type_ == ArgumentType.INTEGER:
            try:
                int(arg)
            except ValueError:
                await DiscordUtilities.send_error_message(ctx, error, footer)
                return False
        elif type_ == ArgumentType.FLOAT:
            try:
                float(arg)
            except ValueError:
                await DiscordUtilities.send_error_message(ctx, error, footer)
                return False
        return True

    @staticmethod
    async def require_str_length_range(ctx: commands.Context,
                                       arg: str,
                                       length_range: tuple[int, int],
                                       error: str,
                                       footer: str) -> bool:
        '''
        Verifica se o tamanho da string está dentro do intervalo.
        '''

        if len(arg) < length_range[0] or len(arg) > length_range[1]:
            await DiscordUtilities.send_error_message(ctx, error, footer)
            return False
        return True

    @staticmethod
    async def require_int_range(ctx: commands.Context,
                                arg: int,
                                range_: tuple[int, int],
                                error: str,
                                footer: str) -> bool:
        '''
        Verifica se o valor inteiro está dentro do intervalo.
        '''

        if arg < range_[0] or arg > range_[1]:
            await DiscordUtilities.send_error_message(ctx, error, footer)
            return False
        return True

    @staticmethod
    async def require_float_range(ctx: commands.Context,
                                  arg: float,
                                  range_: tuple[float, float],
                                  error: str,
                                  footer: str) -> bool:
        '''
        Verifica se o valor float está dentro do intervalo.
        '''

        if arg < range_[0] or arg > range_[1]:
            await DiscordUtilities.send_error_message(ctx, error, footer)
            return False
        return True
