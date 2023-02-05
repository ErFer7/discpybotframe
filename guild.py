# -*- coding: utf-8 -*-

'''
Módulo para os servers.
'''

import os
import json

from datetime import datetime

import discord


class CustomGuild():

    '''
    Definição de um server.
    '''

    # Atributos privados
    _guild: discord.Guild
    _identification: int
    _bot: None
    _settings: dict
    _main_channel: discord.TextChannel
    _voice_channel: discord.VoiceChannel

    # Construtor
    def __init__(self, identification: int, bot) -> None:

        self._identification = identification
        self._bot = bot

        if os.path.exists(os.path.join("Guilds", f"{self._identification}.json")):

            with open(os.path.join("Guilds", f"{self._identification}.json"), 'r+', encoding="utf-8") as settings_file:
                settings_json = settings_file.read()

            self._settings = json.loads(settings_json)
        else:

            self._settings = {"Guild ID": self._identification,
                              "Main channel ID": 0,
                              "Voice channel ID": 0,
                              "Meetings": {}}

        self._guild = self._bot.get_guild(self._identification)
        self._main_channel = self._bot.get_channel(self._settings["Main channel ID"])
        self._voice_channel = self._bot.get_channel(self._settings["Voice channel ID"])

        print(f"[{datetime.now()}][System]: Guild {self._identification} initialized")

    # Métodos
    def write_settings(self) -> None:
        '''
        Escreve as configurações do servidor.
        '''

        with open(os.path.join("Guilds", f"{self._identification}.json"), 'w+', encoding="utf-8") as settings_file:

            settings_json = json.dumps(self._settings, indent=4)
            settings_file.write(settings_json)

        print(f"[{datetime.now()}][System]: Guild {self._identification} saved")

    def get_main_channel(self) -> discord.TextChannel:
        '''
        Retorna o canal principal caso ele exista.
        '''

        if self._bot.get_channel(self._settings["Main channel ID"]) is None:
            self._main_channel = self._guild.text_channels[0]

        return self._main_channel

    def update_main_channel(self, main_channel_id: int) -> None:
        '''
        Atualiza o canal principal.
        '''

        self._settings["Main channel ID"] = main_channel_id
        self._main_channel = self._bot.get_channel(self._settings["Main channel ID"])

        print(f"[{datetime.now()}][System]: The main channel of the guild {self._identification} has been updated")

    def get_voice_channel(self) -> discord.VoiceChannel:
        '''
        Retorna o canal de voz principal caso ele exista.
        '''

        if self._bot.get_channel(self._settings["Voice channel ID"]):
            self._voice_channel = self._guild.voice_channels[0]

        return self._voice_channel

    def update_voice_channel(self, voice_channel_id: int) -> None:
        '''
        Atualiza o canal de voz principal.
        '''

        self._settings["Voice channel ID"] = voice_channel_id
        self._voice_channel = self._bot.get_channel(self._settings["Voice channel ID"])

        print(f"[{datetime.now()}][System]: The main voice channel of the guild "
              f"{self._identification} has been updated")
