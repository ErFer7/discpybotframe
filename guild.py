# -*- coding: utf-8 -*-

'''
Módulo para os servers.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

import json

from abc import abstractmethod
from os.path import exists, join

import discord

if TYPE_CHECKING:
    from discpybotframe.bot import Bot


class Guild():

    '''
    Definição de um server.
    '''

    # Atributos privados
    _identification: int
    _bot: Bot
    _guild: discord.Guild
    _main_channel_id: int
    _voice_channel_id: int
    _main_channel: discord.TextChannel | None
    _voice_channel: discord.VoiceChannel | None

    # Construtor
    def __init__(self, identification: int, bot: Bot) -> None:
        self._identification = identification
        self._bot = bot
        self._guild = self._bot.get_guild(self._identification) # type: ignore
        self._main_channel_id = 0
        self._voice_channel_id = 0
        self._main_channel = None
        self._voice_channel = None

        # Insere a guild no banco de dados se ela não existir
        query = f'''
                    INSERT OR IGNORE INTO Guild (ID, Name, Kick)
                    VALUES ({self._identification}, '{self._guild.name}', FALSE);
                 '''

        self.bot.database_controller.cursor.execute(query)
        self.bot.database_controller.connection.commit()

        query = f'''
                    SELECT Name FROM Guild WHERE ID = {self._identification};
                 '''

        response = self.bot.database_controller.cursor.execute(query)

        if self._guild.name != response.fetchone()[0]:  # type: ignore
            query = f'''
                        UPDATE Guild SET Name = '{self._guild.name}'
                        WHERE ID = {self._identification};
                     '''

            self.bot.database_controller.cursor.execute(query)
            self.bot.database_controller.connection.commit()

        self.load_settings()
        self.load_data()

        self._bot.log('Guild', f'Guild {self._identification} initialized')

    # Getters e Setters
    @property
    def bot(self) -> Bot:
        '''
        Getter do bot.
        '''

        return self._bot

    @property
    def guild(self):
        '''
        Getter do server.
        '''

        return self._guild

    # Métodos
    def load_settings(self) -> None:
        '''
        Lê as configurações do servidor.
        '''

        query = f'''
                    SELECT MainTextChannelID, MainVoiceChannelID FROM Guild
                    WHERE ID = {self._identification};
                '''

        response = self.bot.database_controller.cursor.execute(query)
        self._main_channel_id, self._voice_channel_id = response.fetchone()

        if self._main_channel_id != 0:
            self._main_channel = self._bot.get_channel(self._main_channel_id)  # type: ignore

        if self._voice_channel_id != 0:
            self._voice_channel = self._bot.get_channel(self._voice_channel_id)  # type: ignore

        self._bot.log('Guild', f'Settings for guild {self._identification} loaded')

    @abstractmethod
    def load_data(self) -> None:
        '''
        Lê os dados do servidor.
        '''

    def get_main_channel(self) -> discord.TextChannel | None:
        '''
        Retorna o canal principal caso ele exista.
        '''

        if self._bot.get_channel(self._main_channel_id) is None:
            self._main_channel = self._guild.text_channels[0]

        return self._main_channel

    def update_main_channel(self, main_channel_id: int) -> None:
        '''
        Atualiza o canal principal.
        '''

        self._main_channel_id = main_channel_id
        self._main_channel = self._bot.get_channel(self._main_channel_id)  # type: ignore

        query = f'''
                    UPDATE Guild SET MainTextChannelID = {self._main_channel_id}
                    WHERE ID = {self._identification};
                '''

        self.bot.database_controller.cursor.execute(query)
        self.bot.database_controller.connection.commit()

        self._bot.log('Guild', f'The main channel of the guild {self._identification} has been updated')

    def get_voice_channel(self) -> discord.VoiceChannel | None:
        '''
        Retorna o canal de voz principal caso ele exista.
        '''

        if self._bot.get_channel(self._voice_channel_id):
            self._voice_channel = self._guild.voice_channels[0]

        return self._voice_channel

    def update_voice_channel(self, voice_channel_id: int) -> None:
        '''
        Atualiza o canal de voz principal.
        '''

        self._voice_channel_id = voice_channel_id
        self._voice_channel = self._bot.get_channel(self._voice_channel_id)  # type: ignore

        query = f'''
                    UPDATE Guild SET MainVoiceChannelID = {self._voice_channel_id}
                    WHERE ID = {self._identification};
                '''

        self.bot.database_controller.cursor.execute(query)
        self.bot.database_controller.connection.commit()

        self._bot.log('Guild', f'The main voice channel of the guild {self._identification} has been updated')
