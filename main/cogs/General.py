#!/usr/bin/env python3

# --------------------------------------------------------------------------
#                                 Imports
# --------------------------------------------------------------------------
# Standard library imports
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


# --------------------------------------------------------------------------
#                                 Main
# --------------------------------------------------------------------------
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", pass_context=True)
    async def ping(self, ctx):
        description = f'Pong! {round(self.bot.latency *1000)} ms'
        response = emb.gen_embed_green('Ping!', description)
        await ctx.send(embed=response)


def setup(bot):
    bot.add_cog(General(bot))