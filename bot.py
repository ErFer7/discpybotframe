# -*- coding: utf-8 -*-

'''
Módulo Bot System.
'''

import json

from abc import abstractmethod
from os.path import exists
from time import time_ns
from random import choice, seed
from datetime import datetime
from typing import Callable

import discord

from discord.ext import commands

from .guild import CustomGuild


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
    def load_internal_settings(self, path: str) -> dict:
        '''
        Carrega as configurações internas.
        '''

        if path == "":
            return

        if exists(path):

            with open(path, 'r+', encoding="utf-8") as internal_settings_file:
                internal_settings_json = internal_settings_file.read()

            return json.loads(internal_settings_json)

        print(f"[{datetime.now()}][System]: The loading operation has failed."
              "The file \"internal_settings.json\" should be in the system directory")

        return None

    def set_internal_settings(self, path: str) -> None:
        '''
        Define as configurações internas.
        '''

        print(f"[{datetime.now()}][System]: Loading internal definitions")

        internal_settings = self.load_internal_settings(path)

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
