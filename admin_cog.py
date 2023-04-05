# -*- coding:utf-8 -*-

'''
Módulo para a cog dos comandos de administrador.
'''

from discord.ext import commands

from discpybotframe.cog import Cog
from discpybotframe.utilities import DiscordUtilities


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

        if not self._bot.is_admin(ctx.author.id):
            await DiscordUtilities.send_error_message(ctx, 'Você não tem permissão para usar este comando', 'shutdown')
            return

        # Envia uma mensagem de saída
        await DiscordUtilities.send_message(ctx, 'Encerrando', self._goodbye_message, 'shutdown')

        # Salva todos os servidores
        self.bot.log('AdminCog', 'Saving definitions for every guild')

        self.bot.save_all_guilds()

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

        description = f'''⬩ **{bot_info['Name']} {bot_info['Version']}** - Criada em 2022-03-09

                          ⬩ **Loop HTTP:** {bot_info['HTTP loop']}

                          ⬩ **Latência interna:** {bot_info['Latency']} ms

                          ⬩ **Servidores conectados:** {bot_info['Guild count']}

                          ⬩ **Instâncias de voz:** {bot_info['Voice clients']}'''

        await DiscordUtilities.send_message(ctx, 'Informações', description, 'info')

    @commands.command(name='save')
    async def save(self, ctx) -> None:
        '''
        Salva os servidores.
        '''

        self.bot.log('AdminCog', f'<save> (Author: {ctx.author.name})')

        if not self.bot.is_admin(ctx.author.id):
            await DiscordUtilities.send_error_message(ctx, 'Você não tem permissão para usar este comando', 'shutdown')
            return

        self.bot.save_guild(ctx.guild.id)

        await DiscordUtilities.send_message(ctx, 'Salvando', 'Os dados salvos são únicos para cada servidor', 'save')
