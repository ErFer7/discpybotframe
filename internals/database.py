# -*- coding: utf-8 -*-

'''
Módulo para o banco de dados.
'''

import sqlite3


class DatabaseController():

    '''
    Controle do banco de dados.
    '''

    _connection: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self, path: str) -> None:
        self._connection = sqlite3.connect(path)
        self._cursor = self._connection.cursor()

    @property
    def connection(self) -> sqlite3.Connection:
        '''
        Getter para a conexão.
        '''

        return self._connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        '''
        Getter para o cursor.
        '''

        return self._cursor
