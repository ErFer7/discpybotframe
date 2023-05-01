# -*- coding: utf-8 -*-

'''
Módulo para a validação
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from sys import maxsize
from enum import Enum

from discord.ext import commands

from discpybotframe.utilities import DiscordUtilities

if TYPE_CHECKING:
    from discpybotframe.bot import Bot


class ArgumentType(Enum):

    '''
    Enumerador para os tipos de argumentos.
    '''

    STRING = 0
    INTEGER = 1
    FLOAT = 2


class ArgumentFormat():

    '''
    Classe para definição de formatos de argumentos.
    '''

    _type: ArgumentType
    _range: tuple[int, int] | tuple[float, float] | None
    _length_range: tuple[int, int] | None

    def __init__(self,
                 type_: ArgumentType,
                 range_: tuple[int, int] | tuple[float, float] | None = None,
                 length_range: tuple[int, int] | None = None) -> None:
        self._type = type_
        self._range = range_
        self._length_range = length_range

    def validate(self, arg: str) -> bool:
        '''
        Valida o argumento.
        '''

        match self._type:
            case ArgumentType.STRING:
                if self._length_range is not None:
                    if len(arg) < self._length_range[0] or len(arg) > self._length_range[1]:
                        return False
            case ArgumentType.INTEGER:
                arg_num = None

                try:
                    arg_num = int(arg)
                except ValueError:
                    return False

                if self._range is not None:
                    if arg_num < self._range[0] or arg_num > self._range[1]:
                        return False
            case ArgumentType.FLOAT:
                arg_num = None

                try:
                    arg_num = float(arg)
                except ValueError:
                    return False

                if self._range is not None:
                    if arg_num < self._range[0] or arg_num > self._range[1]:
                        return False

        return True


class Validator():

    '''
    Classe para definição de requisitos de validação.
    '''

    _bot: Bot
    _ctx: commands.Context
    _args: tuple
    _error_message: str
    _footer: str
    _require_adm: bool
    _require_guild: bool
    _arg_format: tuple[ArgumentFormat] | tuple
    _exact_format: bool
    _range: tuple[int, int]

    def __init__(self,
                 bot: Bot,
                 ctx: commands.Context,
                 footer: str,
                 error_message: str = 'Falha no comando',
                 args: tuple = ()) -> None:
        self._bot = bot
        self._ctx = ctx
        self._args = args
        self._error_message = error_message
        self._footer = footer
        self._require_adm = False
        self._require_guild = False
        self._arg_format = ()
        self._exact_format = True
        self._range = (0, maxsize)

    @property
    def bot(self) -> Bot:
        '''
        Getter do bot.
        '''

        return self._bot

    @property
    def ctx(self) -> commands.Context:
        '''
        Getter do contexto.
        '''

        return self._ctx

    @property
    def args(self) -> tuple:
        '''
        Getter dos argumentos.
        '''

        return self._args

    @property
    def error_message(self) -> str:
        '''
        Getter da mensagem de erro.
        '''

        return self._error_message

    @property
    def footer(self) -> str:
        '''
        Getter do rodapé.
        '''

        return self._footer

    def require_conditions(self,
                           adm: bool = False,
                           guild: bool = False) -> None:
        '''
        Define as condições de validação.
        '''

        self._require_adm = adm
        self._require_guild = guild

    def require_arg_format(self,
                           arg_format: tuple[ArgumentFormat] | tuple,
                           exact: bool = True,
                           range_: tuple[int, int] = (0, maxsize)) -> None:
        '''
        Define o formato dos argumentos.
        '''

        self._arg_format = arg_format
        self._exact_format = exact
        self._range = range_

    async def validate_command(self) -> bool:
        '''
        Valida um comando.
        '''

        if self._require_adm and not self._bot.is_admin(self._ctx.author.id):
            await DiscordUtilities.send_error_message(self._ctx, self._error_message, self._footer)
            return False

        if self._require_guild and self._ctx.guild is None:
            await DiscordUtilities.send_error_message(self._ctx, self._error_message, self._footer)
            return False

        arg_size_exact_check = self._exact_format and len(self._arg_format) != len(self._args)
        arg_size_loose_check = len(self._args) < self._range[0] or len(self._args) > self._range[1]

        if arg_size_exact_check or arg_size_loose_check:
            await DiscordUtilities.send_error_message(self._ctx, self._error_message, self._footer)
            return False

        for i, arg in enumerate(self._args):
            if self._exact_format:
                if not self._arg_format[i].validate(arg):
                    await DiscordUtilities.send_error_message(self._ctx, self._error_message, self._footer)
                    return False
            else:
                if not self._arg_format[0].validate(arg):
                    await DiscordUtilities.send_error_message(self._ctx, self._error_message, self._footer)
                    return False

        return True
