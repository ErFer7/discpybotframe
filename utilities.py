# -*- coding:utf-8 -*-

'''
Módulo para o armazenamento de métodos.
'''

import discord


class DiscordUtilities():

    '''
    Utilidades.
    '''

    @staticmethod
    async def send_message(ctx,
                           title: str,
                           description: str,
                           footer: str,
                           error: bool = False,
                           url: str = None) -> None:
        '''
        Envia uma mensagem.
        '''

        embed = None
        prefix = "❱❱❱"
        color = discord.Color.dark_purple()

        if error:
            prefix = "❌ "
            color = discord.Color.red()

        if url is not None:

            embed = discord.Embed(title=f"{prefix} **{title}**",
                                  type="rich",
                                  url=url,
                                  description=description,
                                  color=color)
        else:

            embed = discord.Embed(title=f"{prefix} **{title}**",
                                  type="rich",
                                  description=description,
                                  color=color)

        embed.set_footer(text=f"{footer}")
        await ctx.send(embed=embed)

    @staticmethod
    async def send_error_message(ctx, description: str, footer: str) -> None:
        '''
        Envia um erro.
        '''

        prefix = "❌ "
        color = discord.Color.red()
        embed = discord.Embed(title=f"{prefix} **Erro**",
                                  type="rich",
                                  description=description,
                                  color=color)

        embed.set_footer(text=f"{footer}")
        await ctx.send(embed=embed)
