# -*- coding:utf-8 -*-

'''
Módulo para a cog dos comandos de administrador.
'''

from discord.ext import commands

from discpybotframe.cogs.cog import Cog
from discpybotframe.utils.utilities import DiscordUtilities
from discpybotframe.validation.admin_cog_validator import AdminCogValidator


class AdminCog(Cog):

    '''
    Cog dos comandos de adminstrador.
    '''

    # Atributos privados
    _goodbye_message: str

    def __init__(self, bot, goodbye_message: str) -> None:
        super().__init__(bot)
        self._goodbye_message = goodbye_message
        self.bot.log('AdminCog', 'Administrator command system initialized')

    # Comandos
    @commands.command(name='off')
    async def shutdown(self, ctx) -> None:
        '''
        Desliga o bot.
        '''

        self.bot.log('AdminCog', f'<off> (Author: {ctx.author.name})')

        if not await AdminCogValidator.shutdown_validation(ctx,
                                                           self.bot,
                                                           'Permissão de administrador necessária',
                                                           'shutdown'):
            return

        # Envia uma mensagem de saída
        await DiscordUtilities.send_message(ctx, 'Encerrando', self._goodbye_message, 'shutdown')

        # Encerra o bot
        self.bot.log('AdminCog', 'Exiting')
        await self.bot.close()

    @commands.command(name='info')
    async def info(self, ctx) -> None:
        '''
        Exibe informações.
        '''

        self.bot.log('AdminCog', f'<info> (Author: {ctx.author.name})')

        bot_info = self.bot.get_info()

        description = ''

        for key in bot_info:
            description += f'⬩ **{key}**: {bot_info[key]}\n'

        await DiscordUtilities.send_message(ctx, 'Informações', description, 'info')
