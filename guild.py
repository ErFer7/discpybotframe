# -*- coding: utf-8 -*-

'''
Módulo para os servers.
'''

from __future__ import annotations

import json

from abc import abstractmethod
from os.path import exists, join

import discord

from discpybotframe.bot import Bot


class Guild():

    '''
    Definição de um server.
    '''

    # Atributos privados
    _identification: int
    _bot: Bot
    _guild: discord.Guild
    _settings: dict
    _stored_data: dict
    _main_channel_id: int
    _voice_channel_id: int
    _main_channel: discord.TextChannel | None
    _voice_channel: discord.VoiceChannel | None

    # Construtor
    def __init__(self, identification: int, default_data: dict, bot, guilds_dir: str = 'guilds') -> None:
        self._identification = identification
        self._bot = bot
        self._guild = self._bot.get_guild(self._identification)
        self._settings = {}
        self._stored_data = {}
        self._main_channel_id = 0
        self._voice_channel_id = 0
        self._main_channel = None
        self._voice_channel = None

        self.load_settings(guilds_dir)
        self.load_data(default_data=default_data)

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

    @property
    def settings(self) -> dict:
        '''
        Getter das configurações.
        '''

        return self._settings

    @property
    def stored_data(self) -> dict:
        '''
        Getter dos dados.
        '''

        return self._stored_data

    # Métodos
    def prepare_settings(self) -> dict:
        '''
        Converte as configurações para um formato de dicionário.
        '''

        settings = {'Guild ID': self._identification,
                    'Main channel ID': self._main_channel_id,
                    'Voice channel ID': self._voice_channel_id}

        return settings

    def set_loaded_settings(self, settings: dict) -> None:
        '''
        Aplica as configurações carregadas.
        '''

        self._main_channel_id = settings['Main channel ID']
        self._voice_channel_id = settings['Voice channel ID']
        self._main_channel = self._bot.get_channel(self._main_channel_id) # type: ignore
        self._voice_channel = self._bot.get_channel(self._voice_channel_id) # type: ignore

    def write_settings(self, guilds_dir: str = 'guilds') -> None:
        '''
        Escreve as configurações do servidor.
        '''

        self._settings = self.prepare_settings()

        path = join(guilds_dir, f'{self._identification}_settings.json')

        with open(path, 'w+', encoding='utf-8') as settings_file:
            settings_json = json.dumps(self._settings, indent=4)
            settings_file.write(settings_json)

        self._bot.log('Guild', f'Settings for guild {self._identification} saved')

    def load_settings(self, guilds_dir: str = 'guilds') -> None:
        '''
        Lê as configurações do servidor.
        '''

        settings_path = join(guilds_dir, f'{self._identification}_settings.json')

        if exists(settings_path):
            with open(settings_path, 'r+', encoding='utf-8') as settings_file:
                settings_json = settings_file.read()

            self._settings = json.loads(settings_json)
        else:
            self._settings = {'Guild ID': self._identification,
                              'Main channel ID': 0,
                              'Voice channel ID': 0}

        self.set_loaded_settings(self._settings)

        self._bot.log('Guild', f'Settings for guild {self._identification} loaded')

    @abstractmethod
    def prepare_data(self) -> dict:
        '''
        Converte os dados para um formato de dicionário.
        '''

        return {}

    @abstractmethod
    def set_loaded_data(self, settings: dict) -> None:
        '''
        Aplica as configurações carregadas.
        '''

    def write_data(self, guilds_dir: str = 'guilds') -> None:
        '''
        Escreve os dados do servidor.
        '''

        self._stored_data = self.prepare_data()

        path = join(guilds_dir, f'{self._identification}_data.json')

        with open(path, 'w+', encoding='utf-8') as data_file:
            data_json = json.dumps(self._stored_data, indent=4)
            data_file.write(data_json)

        self._bot.log('Guild', f'Data for guild {self._identification} saved')

    def load_data(self, default_data: dict, guilds_dir: str = 'guilds') -> None:
        '''
        Lê as configurações do servidor.
        '''

        data_path = join(guilds_dir, f'{self._identification}_data.json')

        if exists(data_path):
            with open(data_path, 'r+', encoding='utf-8') as data_file:
                data_json = data_file.read()

            self._stored_data = json.loads(data_json)
        else:
            self._stored_data = default_data

        self.set_loaded_data(self._stored_data)

        self._bot.log('Guild', f'Data for guild {self._identification} loaded')

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
        self._main_channel = self._bot.get_channel(self._settings['Main channel ID']) # type: ignore

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
        self._voice_channel = self._bot.get_channel(self._settings['Voice channel ID']) # type: ignore

        self._bot.log('Guild', f'The main voice channel of the guild {self._identification} has been updated')
