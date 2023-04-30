# -*- coding: utf-8 -*-

'''
Módulo para os servers.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod

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

    # Construtor
    def __init__(self, identification: int, bot: Bot) -> None:
        self._identification = identification
        self._bot = bot
        self._guild = self._bot.get_guild(self._identification) # type: ignore

        # Insere a guild no banco de dados se ela não existir
        query = f'''
                    INSERT OR IGNORE INTO Guild (ID)
                    VALUES ({self._identification});
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
    @abstractmethod
    def load_settings(self) -> None:
        '''
        Lê as configurações do servidor.
        '''

    @abstractmethod
    def load_data(self) -> None:
        '''
        Lê os dados do servidor.
        '''
