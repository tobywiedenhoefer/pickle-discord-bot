import os
from typing import Union

from operations import Operations
from Exceptions import *
from logger import logger
from APIKeys import Keys
from formatter import HelpFormatter

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio


GUILD_ID = Keys.get_key(Keys.guild_id)


class AllCommands:
    play = 'play'


class Command:
    _help = ['help', '']
    _tokens = ['play', 'join', 'leave', 'force-leave']

    def __init__(self, message: discord.Message, bot: commands.Bot, vc: Union[discord.VoiceClient, None]):
        self.message = message
        self.bot = bot
        self.vc = vc

        self.command_line = self.parse_command_line()
        self.cmd_name = self.command_line[0]
        self.token_loc = 1

        # initialized
        # set with shift_token_and_args and in_tokens
        self.token = ''
        self.args = ''
        self.token_used = ''

    async def shift_token_and_args(self):
        """
        Shift token and args.
        """
        self.token_loc += 1
        self.token = self.command_line[self.token_loc-1:self.token_loc]
        if self.token:
            self.token = self.token[0]
        else:
            self.token = ''
        self.args = self.token[self.token_loc:]

    def parse_command_line(self):
        """
        Parse the user's message to create a list of command-line-like elements.
        """
        cl = [arg.lower() for arg in str(self.message.content).split(' ') if arg]
        if not cl:
            raise SentEmptyMessage(str(self.message.author), str(self.message.content))
        return cl

    async def return_message(self, msg: str):
        """
        Send reply to the author.
        """
        await self.message.author.send(msg)

    async def join(self):
        """
        Join the user's voice chat, if they are in one.
        """
        logger.info(f'{self.message.author} requested bot to join {self.bot.get_guild(GUILD_ID)}.')
        await self.return_message('Joining voice chat...')

        logger.debug('Getting voice client...')

        if self.vc and self.vc.is_connected():
            logger.debug('Voice client found. Exiting early.')
            return None

        guild = self.bot.get_guild(int(GUILD_ID))
        if not guild:
            raise NoneType(Operations.connect_to_guild, 'guild')

        member = await guild.fetch_member(self.message.author.id)
        channel = member.voice.channel

        self.vc = await channel.connect()
        await self.return_message('Successfully connected!')

    async def force_leave(self):
        await self.join()
        await self.leave_vc()

    async def leave_vc(self):
        """
        Leave voice chat, if connected.
        """
        if self.vc and self.vc.is_connected():
            guild = self.bot.get_guild(int(GUILD_ID))
            await guild.voice_client.disconnect()
            await self.return_message('Successfully disconnected.')
        await self.return_message(
            "If I didn't leave the voice channel, you can always use the less-pleasant 'force-leave' command."
        )

    async def in_tokens(self, tokens: list, cmd=None) -> bool:
        """
        Returns a boolean depending on if the class's set token is in the list of tokens.
        """
        if not cmd:
            cmd = self.token
        for token in tokens:
            if token == cmd:
                self.token_used = cmd
                return True
        return False

    async def help(self, tokens: list):
        help_formatter = HelpFormatter(tokens=tokens, parsed_commands=self.command_line)
        await self.return_message(str(help_formatter))

    async def return_error_message(self):
        logger.info(f"Message not understood. User {self.message.author} sent {self.command_line}")
        await self.return_message("I don't understand. Try typing 'help' to get started.")

    async def exec(self):
        if await self.in_tokens(Command._tokens, self.cmd_name):
            if self.token_used == 'play':
                logger.debug("Transferring to Play object.")
                self.__class__ = Play
                await self.shift_token_and_args()
                await self.exec()
            elif self.token_used == 'join':
                await self.join()
            elif self.token_used == 'leave':
                await self.leave_vc()
            elif self.token_used == 'force-leave':
                await self.force_leave()
        elif await self.in_tokens(Command._help, self.cmd_name):
            await self.help(Command._tokens)
        else:
            await self.return_error_message()


class Play(Command):
    _tokens = ["sound"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def exec(self):
        if await self.in_tokens(Play._tokens):
            if self.token_used == 'sound':
                self.__class__ = Sound
                logger.debug("Transferring to Sound object.")
            await self.shift_token_and_args()
            await self.exec()
        elif await self.in_tokens(Command._help):
            await self.help(Play._tokens)
        else:
            await self.return_error_message()


class Sound(Play):
    _tokens = [file.split('.')[0].lower() for file in os.listdir('./sound_effects')]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def play_sound(self):
        src = FFmpegPCMAudio(f'./sound_effects/{self.token}.mp3')
        self.vc.play(source=src)

    async def exec(self):
        if await self.in_tokens(Sound._tokens):
            await self.join()
            self.play_sound()
            await self.return_message(f'Playing {self.token}')
        elif await self.in_tokens(Command._help):
            await self.help(Sound._tokens)
