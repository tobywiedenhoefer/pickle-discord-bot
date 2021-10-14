from typing import Union

from operations import Operations
from Exceptions import *
from logger import logger
from APIKeys import Keys

import discord
from discord.ext import commands

GUID_ID = Keys.get_key(Keys.token)


class AllCommands:
    play = 'play'


class Command:
    _help = ['help', '--help', '-h']

    def __init__(self, message: discord.Message, bot: commands.Bot, vc: Union[discord.VoiceClient, None]):
        self.message = message
        self.bot = bot
        self.vc = vc

        self.command_line = self.parse_command_line()
        self.cmd_name = self.command_line[0]
        self.token = self.command_line[1:]
        self.args = self.token[1:]

    def parse_command_line(self):
        cl = [arg.lower() for arg in str(self.message.content).split(' ') if arg]
        if not cl:
            raise SentEmptyMessage(str(self.message.author), str(self.message.content))
        return cl

    async def return_message(self, msg:str):
        await self.message.author.send(msg)

    async def join(self):
        logger.info(f'{self.message.author} requested bot to join {self.bot.get_guild(int(GUID_ID))}.')
        await self.return_message('Joining voice chat...')

        logger.debug('Getting voice client...')

        if self.vc and self.vc.is_connected():
            logger.debug('Voice client found. Exiting early.')
            return None

        guild = self.bot.get_guild(int(GUID_ID))
        if not guild:
            raise NoneType(Operations.connect_to_guild, 'guild')

        member = await guild.fetch_member(self.message.author.id)
        channel = member.voice.channel

        self.vc = await channel.connect()
        await self.return_message('Successfully connected!')

    async def leave_vc(self, message: discord.Message):
        if self.vc and self.vc.is_connected():
            guild = self.bot.get_guild(int(GUID_ID))
            await guild.voice_client.disconnect()
            await self.return_message('Successfully disconnected.')
