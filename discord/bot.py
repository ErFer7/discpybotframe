# -*- coding: utf-8 -*-

'''
Módulo Bot System.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

import platform
import json

from abc import abstractmethod
from os.path import exists
from time import time_ns
from random import choice, seed
from datetime import datetime

import discord

from discord.ext import commands, tasks
from discord.ext.commands import HelpCommand

from discpybotframe.internals.database import DatabaseController

if TYPE_CHECKING:
    from discpybotframe.discord.guild import Guild


class Bot(commands.Bot):

    '''
    Bot customizado.
    '''

    # Atributos privados
    _name: str
    _version: str
    _token: str
    _admins_id: list
    _users: dict
    _custom_guilds: dict
    _activities: list[str]
    _custom_ready: bool
    _database_controller: DatabaseController | None
    _init_time: datetime

    def __init__(self,
                 command_prefix: str,
                 help_command: HelpCommand,
                 name: str,
                 settings_file: str,
                 intents,
                 version: str,
                 database_path: str = '',
                 dev_env: bool = False) -> None:

        super().__init__(command_prefix=command_prefix, help_command=help_command, intents=intents)

        self._name = name
        self._version = version
        self._custom_guilds = {}
        self._users = {}
        self._admins_id = []
        self._token = ''
        self._activities = ['Error']
        self._custom_ready = False
        self._database_controller = None
        self._init_time = datetime.now()

        if database_path != '':
            self._database_controller = DatabaseController(database_path)

        environment = 'development' if dev_env else 'production'

        self.log('Bot', f'Initializing {self._name} {self._version} with {environment} profile')
        self.log('Bot', 'Initializing the RNG')

        seed(time_ns())
        self.set_internal_settings(settings_file, dev_env)

    # Getters e Setters
    @property
    def custom_guilds(self) -> dict:
        '''
        Getter dos servers.
        '''

        return self._custom_guilds

    @property
    def database_controller(self) -> DatabaseController | None:
        '''
        Getter do database controller.
        '''

        return self._database_controller

    # Loops
    @tasks.loop(seconds=3600.0)  # 1 hora
    async def activity(self) -> None:
        '''
        Salva os dados.
        '''

        self.log('Bot', 'Setting activity automatically')
        await self.set_activity()

    # Eventos
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        '''
        Evento de "dados preparados".
        '''

        self.log('Bot', 'Ready')
        await self.prepare_data()

        self.activity.start()

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        '''
        Evento de conexão.
        '''

        self.log('Bot', 'Connected')

    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        '''
        Evento de desconexão.
        '''

        self.log('Bot', 'Disconnected')

    @commands.Cog.listener()
    async def on_resumed(self) -> None:
        '''
        Evento de retorno.
        '''

        self.log('Bot', 'Resumed')

    @commands.Cog.listener()
    async def on_guild_join(self, guild) -> None:
        '''
        Evento para a entrada em um servidor.
        '''

        self.add_guild(guild.id)
        self.log('Bot', f'Joined guild {guild.name}.')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild) -> None:
        '''
        Evento para a saída de um servidor.
        '''

        self.remove_guild(guild.id)
        self.log('Bot', f'Left guild {guild.name}.')

    # Métodos
    @abstractmethod
    async def setup_hook(self) -> None:
        '''
        Pré-setup.
        '''

    @abstractmethod
    def add_guild(self, guild_id: int) -> None:
        '''
        Adiciona um servidor.
        '''

    @abstractmethod
    def remove_guild(self, guild_id: int) -> None:
        '''
        Remove um servidor.
        '''

    def load_guilds(self) -> None:
        '''
        Carrega os servidores.
        '''

        self.log('Bot', 'Loading guilds definitions...')

        for guild in self.guilds:
            self.add_guild(guild.id)

    async def prepare_data(self) -> None:
        '''
        Prepara os dados.
        '''

        if not self._custom_ready:
            self._custom_ready = True
        else:
            return

        self.log('Bot', 'Waiting...')
        await self.wait_until_ready()

        self.load_guilds()

        if self.user is not None:
            self.log('Bot', f'{self._name} {self._version} ready to operate')
            self.log('Bot', f'Logged as {self.user.name}, with the id: {self.user.id}')
        else:
            self.log('Bot', 'Failed to get the user data')

    async def set_activity(self, activity: str = '', status: discord.Status = discord.Status.online) -> None:
        '''
        Define a atividade.
        '''

        if activity != '':
            await self.change_presence(activity=discord.Game(name=activity), status=status)
        else:
            await self.change_presence(activity=discord.Game(name=choice(self._activities)), status=status)

    # Métodos
    def load_internal_settings(self, path: str) -> dict | None:
        '''
        Carrega as configurações internas.
        '''

        if path == "":
            return None

        if exists(path):
            with open(path, 'r+', encoding='utf-8') as internal_settings_file:
                internal_settings_json = internal_settings_file.read()

            return json.loads(internal_settings_json)

        self.log('Bot',
                 'The loading operation has failed. The file '
                 '"internal_settings.json" should be in the system directory')

        return None

    def set_internal_settings(self, path: str, dev_env: bool) -> None:
        '''
        Define as configurações internas.
        '''

        self.log('Bot', 'Loading internal definitions')

        internal_settings = self.load_internal_settings(path)

        if internal_settings is not None:
            self._admins_id = list(map(int, internal_settings['adm_id']))

            if dev_env:
                self._token = internal_settings['devenv_token']
            else:
                self._token = internal_settings['token']

            self._activities = internal_settings['activities']
        else:
            self.log('Bot', 'Failed set internal definitions')

    def run(self, *args: tuple, **kwargs: tuple) -> None:
        '''
        Roda o bot.
        '''

        args += (self._token,)  # type: ignore

        return super().run(*args, **kwargs)  # type: ignore

    def is_admin(self, author_id: int) -> bool:
        '''
        Checa se o autor é um administrador.
        '''

        return author_id in self._admins_id

    def get_info(self) -> dict:
        '''
        Retorna um dicionário com informações.
        '''

        info = {'Name': self._name,
                'Version': self._version,
                'HTTP loop': self.http,
                'Latency': self.latency,
                'Guild count': len(self.guilds),
                'Voice clients': self.voice_clients,
                'Uptime': datetime.now() - self._init_time,
                'Platform': platform.platform(),
                'Processor': platform.processor(),
                'Architecture': platform.machine(),
                'Python version': platform.python_version()}

        return info

    def get_custom_guild(self, guild_id: int) -> Guild:
        '''
        Retorna um server personalizado.
        '''

        return self._custom_guilds[str(guild_id)]

    def log(self, origin: str, message: str) -> None:
        '''
        Exibe uma mensagem no console.
        '''

        print(f"[{datetime.now()}][{origin}]: {message}")
