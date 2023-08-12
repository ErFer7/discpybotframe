# -*- coding: utf-8 -*-

'''
Módulo para os servers.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod

import discord

if TYPE_CHECKING:
    from discpybotframe.discord.bot import Bot


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

    def load(self) -> None:
        '''
        Carrega informações na ordem correta.
        '''

        self.load_settings()
        self.load_data()

    def remove(self) -> None:
        '''
        Remove informações na ordem correta.
        '''

        self.remove_data()
        self.remove_settings()

    # Métodos
    def load_settings(self) -> None:
        '''
        Lê as configurações do servidor.
        '''

        if self.bot.database_controller is not None:
            query = f'''
                        INSERT OR IGNORE INTO Guild (ID)
                        VALUES ({self._identification});
                    '''

            self.bot.database_controller.cursor.execute(query)
            self.bot.database_controller.connection.commit()

    @abstractmethod
    def load_data(self) -> None:
        '''
        Lê os dados do servidor.
        '''

    def remove_settings(self) -> None:
        '''
        Remove as configurações do servidor.
        '''

        if self.bot.database_controller is not None:
            query = f'''
                        DELETE FROM Guild
                        WHERE ID = {self._identification};
                    '''

            self.bot.database_controller.cursor.execute(query)
            self.bot.database_controller.connection.commit()


    @abstractmethod
    def remove_data(self) -> None:
        '''
        Remove os dados do servidor.
        '''
