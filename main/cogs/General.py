#!/usr/bin/env python3

# --------------------------------------------------------------------------
#                                 Imports
# --------------------------------------------------------------------------
# Standard library imports
import logging
import sys
import os

# Third party imports
import discord # noqa
from discord.ext import commands

# Local application imports
# Enabling local imports
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
from settings import embeds as emb # noqa


log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
#                                 Main
# --------------------------------------------------------------------------
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", pass_context=True, help="Replies with the latency to the bot.")
    async def ping(self, ctx):
        description = f'Pong! {round(self.bot.latency *1000)} ms'
        response = emb.gen_embed_green('Ping!', description)
        await ctx.send(embed=response)

    @commands.command(name='source', help="Gets the bot's source code and trello page.")
    async def source(self, ctx, *args):
        trello = ''
        github = 'https://github.com/NekroDarkmoon/Zen-Public/'

        for arg in args:
            if arg == '-t':
                trello = 'https://trello.com/b/rej22uVl/zen'

        try:
            await ctx.send(github + '\n' + trello)
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(General(bot))
