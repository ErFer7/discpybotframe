# -*- coding:utf-8 -*-

'''
Módulo para a cog dos comandos de configurações.
'''

from datetime import datetime

from discord.ext import commands

from discpybotframe.utilities import DiscordUtilities


class SettingsCog(commands.Cog):

    '''
    Cog dos comandos de configurações.
    '''

    # Atributos privados
    _bot: None

    def __init__(self, bot) -> None:
        self._bot = bot

        print(f"[{datetime.now()}][Settings]: Settings system initialized")

    # Comandos
    @commands.command(name="channel", aliases=("canal", "ch", "ca"))
    async def channel_update(self, ctx) -> None:
        '''
        Define o canal principal de bots.
        '''

        print(f"[{datetime.now()}][Settings]: <channel_update> (Author: {ctx.author.name})")

        if len(ctx.message.channel_mentions) != 1:
            await DiscordUtilities.send_error_message(ctx, "Mencione um canal com #canal!", "channel")
            return

        self._bot.get_custom_guild(ctx.guild.id).update_main_channel(ctx.message.channel_mentions[0].id)

        await DiscordUtilities.send_message(ctx,
                                            "Canal redefinido",
                                            f"Novo canal de textos: {ctx.message.channel_mentions[0].name}",
                                            "channel")

    @commands.command(name="voice_channel", aliases=("canal_voz", "vch", "cav"))
    async def voice_channel_update(self, ctx, *args) -> None:
        '''
        Define o canal de voz do bot.
        '''

        print(f"[{datetime.now()}][Settings]: <voice_channel_update> (Author: {ctx.author.name})")

        if args is None:
            await DiscordUtilities.send_error_message(ctx, "Erro crítico nos argumentos!", "voice_channel")
            return

        if len(args) != 1:
            await DiscordUtilities.send_error_message(ctx, "Especifique o nome do canal de voz!", "voice_channel")
            return

        channel_found = False

        for channel in ctx.guild.voice_channels:
            if channel.name == args[0]:
                self._bot.get_custom_guild(ctx.guild.id).update_voice_channel(channel.id)
                channel_found = True

        if channel_found:
            await DiscordUtilities.send_message(ctx,
                                                "Canal de voz redefinido",
                                                f"Novo canal de voz: {args[0]}",
                                                "voice_channel")
        else:
            await DiscordUtilities.send_error_message(ctx, "Canal não encontrado!", "voice_channel")
