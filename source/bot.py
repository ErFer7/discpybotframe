# -*- coding: utf-8 -*-

'''
Módulo Bot System
'''

import os
import json

from abc import abstractmethod
from os.path import exists, join
from time import time_ns
from random import choice, seed
from datetime import datetime
from typing import Callable

import discord

from discord.ext import commands


class CustomBot(commands.Bot):

    '''
    Bot customizado.
    '''

    # Atributos privados
    _name: str
    _version: str
    _token: str
    _admins_id: int
    _users: dict
    _guilds: dict
    _activity_str: str
    _ready: bool

    # Construtor
    def __init__(self,
                 command_prefix: str,
                 help_command: Callable,
                 name: str,
                 settings_file: str,
                 version: str) -> None:

        super().__init__(command_prefix=command_prefix, help_command=help_command, intents=None)

        self._name = name
        self._version = version
        self._guilds = {}
        self._users = {}
        self._admins_id = []
        self._token = ""
        self._activity_str = ""
        self._ready = False

        print(f"[{datetime.now()}][System]: Initializing {self._name} {self._version}")
        print(f"[{datetime.now()}][System]: Initializing the RNG")

        seed(time_ns())
        self.set_internal_settings(settings_file)

    # Métodos assícronos
    @abstractmethod
    async def setup_hook(self) -> None:
        '''
        Pré-setup.
        '''

    async def prepare_data(self) -> None:
        '''
        Prepara os dados e a presença.
        '''

        if not self._ready:
            self._ready = True
        else:
            return

        print(f"[{datetime.now()}][System]: Waiting...")
        await self.wait_until_ready()

        print(f"[{datetime.now()}][System]: Loading guilds definitions")
        for guild in self.guilds:
            self._guilds[str(guild.id)] = CustomGuild(guild.id, self)

        print(f"[{datetime.now()}][System]: {self._name} {self._version} ready to operate")
        print(f"[{datetime.now()}][System]: Logged as {self.user.name}, with the id: {self.user.id}")

        await self.set_activity()

    async def set_activity(self, activity: str = None) -> None:
        '''
        Define a atividade.
        '''

        if activity is not None:
            await self.change_presence(activity=discord.Game(name=activity))
        else:
            await self.change_presence(activity=discord.Game(name=self._activity_str))

    # Métodos
    def load_internal_settings(self, file_name: str) -> dict:
        '''
        Carrega as configurações internas.
        '''

        if file_name == "":
            return

        if exists(join("System", file_name)):

            with open(join("System", file_name), 'r+', encoding="utf-8") as internal_settings_file:
                internal_settings_json = internal_settings_file.read()

            return json.loads(internal_settings_json)

        print(f"[{datetime.now()}][System]: The loading operation has failed."
              "The file \"internal_settings.json\" should be in the system directory")

        return None

    def set_internal_settings(self, settings_file: str) -> None:
        '''
        Define as configurações internas.
        '''

        print(f"[{datetime.now()}][System]: Loading internal definitions")

        internal_settings = self.load_internal_settings(settings_file)

        self._admins_id = list(map(int, internal_settings["ADM_ID"]))
        self._token = internal_settings["TOKEN"]
        self._activity_str = choice(internal_settings["Activities"])

    def run(self, *args: tuple, **kwargs: tuple) -> None:
        '''
        Roda o bot.
        '''

        args += (self._token,)

        return super().run(*args, **kwargs)

    def write_settings_for_guild(self, guild_id: int) -> None:
        '''
        Salva as configurações do servidor específico.
        '''

        self._guilds[str(guild_id)].write_settings()

    def write_settings_for_all(self) -> None:
        '''
        Salva as configurações de todos os servidores.
        '''

        for guild in self._guilds.values():
            guild.write_settings()

    def is_admin(self, author_id: int) -> bool:
        '''
        Checa se o autor é um administrador.
        '''

        return author_id in self._admins_id

    def get_info(self) -> dict:
        '''
        Retorna um dicionário com informações.
        '''

        info = {"Name": self._name,
                "Version": self._version,
                "HTTP loop": self.http,
                "Latency": self.latency,
                "Guild count": len(self.guilds),
                "Voice clients": self.voice_clients}

        return info

    def get_custom_guild(self, guild_id: int):
        '''
        Retorna um server personalizado.
        '''

        return self._guilds[str(guild_id)]


class CustomGuild():

    '''
    Definição de um server.
    '''

    # Atributos privados
    _guild: discord.Guild
    _identification: int
    _bot: CustomBot
    _settings: dict
    _main_channel: discord.TextChannel
    _voice_channel: discord.VoiceChannel

    # Construtor
    def __init__(self, identification: int, bot: CustomBot) -> None:

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
        self._main_channel = self._bot.get_channel(
            self._settings["Main channel ID"])

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
        self._voice_channel = self._bot.get_channel(
            self._settings["Voice channel ID"])

        print(f"[{datetime.now()}][System]: The main voice channel of the guild "
              f"{self._identification} has been updated")
