# -*- coding: utf-8 -*-

'''
Módulo para o controle de conexões aos canais de voz e à reprodução de áudios.
'''

from asyncio import Lock

import discord


class VoiceController():

    '''
    Controlador de voz.
    '''

    _bot: None
    _voice_client: discord.VoiceClient
    _voice_channel: discord.VoiceChannel
    _ffmpeg_path: str
    _lock: Lock

    def __init__(self, bot, ffmpeg_path: str) -> None:

        self._bot = bot
        self._voice_client = None
        self._voice_channel = None
        self._ffmpeg_path = ffmpeg_path
        self._lock = Lock()

    def play_audio(self, source: str) -> None:
        '''
        Toca um áudio.
        '''

        if self._voice_client is not None and self._voice_client.is_connected():

            if self._voice_client.is_playing():
                self._voice_client.stop()

            self._voice_client.play(discord.FFmpegPCMAudio(source=source, executable=self._ffmpeg_path))

    async def connect(self, voice_channel: discord.VoiceChannel) -> None:
        '''
        Conecta-se a um canal.
        '''

        await self._lock.acquire()
        try:
            if voice_channel is not None and self._voice_client is None:
                self._voice_channel = voice_channel
                self._voice_client = await voice_channel.connect()

                if self._voice_client is not None and self._voice_client.is_connected():
                    if self._voice_client.is_playing():
                        self._voice_client.stop()
        finally:
            self._lock.release()

    async def disconnect(self) -> None:
        '''
        Desconecta-se de um canal.
        '''

        await self._lock.acquire()
        try:
            if self._voice_client is not None and self._voice_client.is_connected():
                await self._voice_client.disconnect()
                self._voice_client = None
                self._voice_channel = None
        finally:
            self._lock.release()

    async def remove_all_members(self) -> None:
        '''
        Remove todos os membros de um canal.
        '''

        await self._lock.acquire()
        try:
            if self._voice_client is not None and self._voice_client.is_connected():
                for member in self._voice_channel.members:
                    if member != self._bot:
                        await member.move_to(None)
        finally:
            self._lock.release()
