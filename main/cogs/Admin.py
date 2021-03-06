#!/usr/bin/env python3

# --------------------------------------------------------------------------
#                                 Imports
# --------------------------------------------------------------------------
# Standard library imports
import asyncpg
import datetime
import logging
import sys
import os
import traceback

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
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #                                   Kick
    @commands.command(name="kick", pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a member from the server.

        `kick 'username'/@mention/id reason`"""

        if reason is None:
            reason = f"Kicked by {ctx.author}\nID: {ctx.author.id}"

        e = emb.gen_embed_white(f'Kicked {member}', reason)
        e.set_thumbnail(url=member.avatar_url)

        try:
            await ctx.guild.kick(member, reason=reason)
            await ctx.message.delete()
            await ctx.send(embed=e)
        except Exception as e:
            log.warning(e)
            log.error(traceback.format_exc())
            embed = emb.gen_embed_orange('Error', e)
            await ctx.send(embed=embed)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #                                   Ban
    @commands.command(name="ban", pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a member from the server.

        `ban 'username'/@mention/id reason`"""

        if reason is None:
            reason = f"Banned by {ctx.author}\nID: {ctx.author.id}"

        e = emb.gen_embed_white(f'Banned {member}', reason)

        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.message.delete()
            await ctx.send(embed=e)
        except Exception as e:
            log.warning(e)
            log.error(traceback.format_exc())
            embed = emb.gen_embed_orange('Error', e)
            await ctx.send(embed=embed)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #                                   Unban
    @commands.command(name="unban", pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        """Unbans a member from the server

        `unban 'username'/@mention/id reason`"""

        if reason is None:
            reason = f"Unbanned by {ctx.author}.\nID: {ctx.author.id}"

        e = emb.gen_embed_white(f'Unbanned {member}', reason)

        try:
            await ctx.guild.unban(member, reason=reason)
            await ctx.message.delete()
            await ctx.send(embed=e)
        except Exception as e:
            log.warning(e)
            log.error(traceback.format_exc())
            embed = emb.gen_embed_orange('Error', e)
            await ctx.send(embed=embed)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #                                   Userinfo
    @commands.command(name="userinfo", pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def userinfo(self, ctx, *, member: discord.Member):
        """Displays information about a user

        `userinfo 'username'/@mention/id`"""

        try:
            # Variables
            conn = self.bot.pool
            roles = [role.name.replace('@', '@\u200b') for role in getattr(member, 'roles', [])]
            shared = sum(g.get_member(member.id) is not None for g in self.bot.guilds)

            embed = discord.Embed()
            embed.set_author(name=member)
            embed.add_field(name='ID', value=member.id, inline=True)
            embed.add_field(name='Servers', value=shared, inline=True)
            embed.add_field(name='Joined', value=getattr(member, 'joined_at', None), inline=False)
            embed.add_field(name='Created', value=member.created_at, inline=False)

            voice = getattr(member, 'voice', None)
            if voice is not None:
                vc = voice.channel
                other_people = len(vc.members) - 1
                voice = f'{vc.name} with {other_people} others' if other_people else f'{vc.name} by themselves'
                embed.add_field(name='Voice', value=voice, inline=False)

            if roles:
                embed.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else
                                f'{len(roles)} roles', inline=False)

            # Get last message
            sql = """SELECT * FROM lb WHERE server_id= $1 AND user_id = $2; """
            data = await conn.fetchrow(sql, member.guild.id, member.id)
            if data is not None:
                last_msg = data[2]
                last_msg = last_msg.strftime("%c")
                embed.add_field(name="Last Message at", value=last_msg, inline=False)

            color = member.colour
            if color.value:
                embed.color = color
            else:
                embed.color = 0xf2f6f7

            if member.avatar:
                embed.set_thumbnail(url=member.avatar_url)

            if isinstance(member, discord.User):
                embed.set_footer(text='This member is not in this server.')

            await ctx.send(embed=embed)

        except Exception as e:
            log.warning(e)
            log.error(traceback.format_exc())
            await ctx.send(embed=emb.gen_embed_orange('Error', e))


def setup(bot):
    bot.add_cog(Admin(bot))
