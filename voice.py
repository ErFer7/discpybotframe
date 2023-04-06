# -*- coding: utf-8 -*-

'''
Módulo para o controle de conexões aos canais de voz e à reprodução de áudios.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from discpybotframe.bot import Bot


class VoiceController():

    '''
    Controlador de voz.

    Atualmente, o controlador de voz suporta apenas um canal de voz.
    '''

    _bot: Bot
    _ffmpeg_path: str

    def __init__(self, bot, ffmpeg_path: str) -> None:
        self._bot = bot
        self._ffmpeg_path = ffmpeg_path

    def play_audio(self, source: str) -> None:
        '''
        Toca um áudio.
        '''

        voice_client: discord.VoiceClient | None = None

        if len(self._bot.voice_clients) > 0:
            voice_client = self._bot.voice_clients[0] # type: ignore

        self._bot.log('VoiceController', f'<play_audio> Playing audio on voice client {voice_client}')

        if voice_client is not None and voice_client.is_connected():
            if voice_client.is_playing():
                voice_client.stop()

            voice_client.play(discord.FFmpegPCMAudio(source=source, executable=self._ffmpeg_path))

    async def connect(self, voice_channel: discord.VoiceChannel) -> None:
        '''
        Conecta-se a um canal.
        '''

        voice_client: discord.VoiceClient | None = None

        if len(self._bot.voice_clients) > 0:
            voice_client = self._bot.voice_clients[0] # type: ignore

        self._bot.log('VoiceController', f'<connect> connecting to voice channel {voice_channel}')

        if voice_channel is not None and voice_client is None:
            voice_client = await voice_channel.connect()

            if voice_client is not None and voice_client.is_connected():
                if voice_client.is_playing():
                    voice_client.stop()

    async def disconnect(self) -> None:
        '''
        Desconecta-se de um canal.
        '''

        voice_client: discord.VoiceClient | None = None

        if len(self._bot.voice_clients) > 0:
            voice_client = self._bot.voice_clients[0] # type: ignore

        self._bot.log('VoiceController', f'<disconnect> disconnecting voice client {voice_client}')

        if voice_client is not None and voice_client.is_connected():
            await voice_client.disconnect()

    async def get_members(self) -> list[discord.Member]:
        '''
        Retorna uma lista com todos os membros de um canal.
        '''

        voice_client: discord.VoiceClient | None = None

        if len(self._bot.voice_clients) > 0:
            voice_client = self._bot.voice_clients[0] # type: ignore

        self._bot.log('VoiceController',
                      f'<get_members> getting members from channel in voice client {voice_client}')

        if voice_client is not None and voice_client.is_connected():
            return voice_client.channel.members

        return []

    async def remove_all_members(self) -> None:
        '''
        Remove todos os membros de um canal.
        '''

        voice_client: discord.VoiceClient | None = None

        if len(self._bot.voice_clients) > 0:
            voice_client = self._bot.voice_clients[0] # type: ignore

        self._bot.log('VoiceController',
                      f'<remove_all_members> removing all members from channel in voice channel {voice_client}')

        if voice_client is not None and voice_client.is_connected():
            for member in voice_client.channel.members:
                if member.id != self._bot.user.id:  # type: ignore
                    await member.move_to(None)
