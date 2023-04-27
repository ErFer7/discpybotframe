# -*- coding:utf-8 -*-

'''
Módulo para a cog dos comandos de configurações.
'''

from discord.ext import commands

from discpybotframe.utilities import DiscordUtilities
from discpybotframe.cog import Cog


class SettingsCog(Cog):

    '''
    Cog dos comandos de configurações.
    '''

    def __init__(self, bot) -> None:
        super().__init__(bot)
        self.bot.log('SettingsCog', 'Settings system initialized')

    # Comandos
    @commands.command(name='channel', aliases=('canal', 'ch', 'ca'))
    async def channel_update(self, ctx) -> None:
        '''
        Define o canal principal de bots.
        '''

        self.bot.log('SettingsCog', f'<channel_update> (Author: {ctx.author.name}')

        require_guild = (True, 'Este comando só pode ser usado em servidores', 'channel')
        require_text_channel = (True, 'Mencione um canal com #canal!', 'channel')

        if not await self.validate_command(ctx,
                                           require_guild=require_guild,
                                           require_text_channel=require_text_channel):
            return

        self._bot.get_custom_guild(ctx.guild.id).update_main_channel(ctx.message.channel_mentions[0].id)

        await DiscordUtilities.send_message(ctx,
                                            'Canal redefinido',
                                            f'Novo canal de textos: {ctx.message.channel_mentions[0].name}',
                                            'channel')

    @commands.command(name='voice_channel', aliases=('canal_voz', 'vch', 'cav'))
    async def voice_channel_update(self, ctx, *args) -> None:
        '''
        Define o canal de voz do bot.
        '''

        self.bot.log('SettingsCog', f'<voice_channel_update> (Author: {ctx.author.name}')

        require_guild = (True, 'Este comando só pode ser usado em servidores', 'voice_channel')
        require_voice_channel = (True, 'Especifique o nome do canal de voz!', 'voice_channel')
        require_args = (1, 'Especifique o nome do canal de voz!', 'voice_channel')

        if not await self.validate_command(ctx,
                                           args=args,
                                           require_guild=require_guild,
                                           require_voice_channel=require_voice_channel,
                                           require_args=require_args):
            return

        guild = ctx.guild

        for channel in guild.voice_channels:
            if channel.name == args[0]:
                self._bot.get_custom_guild(ctx.guild.id).update_voice_channel(channel.id)

        await DiscordUtilities.send_message(ctx,
                                            'Canal de voz redefinido',
                                            f'Novo canal de voz: {args[0]}',
                                            'voice_channel')
