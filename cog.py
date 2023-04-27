# -*- coding: utf-8 -*-

'''
Módulo para a definição de uma cog.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext import commands

from discpybotframe.utilities import DiscordUtilities

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

    async def validate_command(self,
                               ctx: commands.Context,
                               args: tuple[str, ...] | None = None,
                               require_adm: tuple[bool, str, str] = (False, '', ''),
                               require_guild: tuple[bool, str, str] = (False, '', ''),
                               require_text_channel: tuple[bool, str, str] = (False, '', ''),
                               require_voice_channel: tuple[bool, str, str] = (False, '', ''),
                               require_args: tuple[int, str, str] = (0, '', ''),
                               require_args_type: tuple | None = None) -> bool:
        '''
        Valida um comando.
        '''

        if require_adm[0] and not self._bot.is_admin(ctx.author.id):
            await DiscordUtilities.send_error_message(ctx, require_adm[1], require_adm[2])
            return False

        if require_guild[0] and ctx.guild is None:
            await DiscordUtilities.send_error_message(ctx, require_guild[1], require_guild[2])
            return False

        if require_args[0] > 0:

            if args is None:
                await DiscordUtilities.send_error_message(ctx, require_args[1], require_args[2])
                return False

            if len(args) != require_args[0]:
                await DiscordUtilities.send_error_message(ctx, require_args[1], require_args[2])
                return False

        if require_args_type is not None:

            if args is None:
                return False

            for i, arg in enumerate(args):
                if require_args_type[i] == 'int':
                    try:
                        int(arg)
                    except ValueError:
                        await DiscordUtilities.send_error_message(ctx, require_args[1], require_args[2])
                        return False
                elif require_args_type[i] == 'float':
                    try:
                        float(arg)
                    except ValueError:
                        await DiscordUtilities.send_error_message(ctx, require_args[1], require_args[2])
                        return False

        if require_text_channel[0] and len(ctx.message.channel_mentions) != 1:
            await DiscordUtilities.send_error_message(ctx, require_text_channel[1], require_text_channel[2])
            return False

        if require_voice_channel[0]:
            channel_found = False

            if args is not None:
                for channel in ctx.guild.voice_channels:  # type: ignore
                    if channel.name == args[0]:
                        channel_found = True

            if not channel_found:
                await DiscordUtilities.send_error_message(ctx, require_voice_channel[1], require_voice_channel[2])
                return False

        return True
