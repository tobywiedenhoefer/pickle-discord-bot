# base packages
import os
from typing import Union

# local packages
from logger import logger
from APIKeys import Keys
from Exceptions import ExceptionStrings
from Exceptions import NotLongEnough, NoneType
from operations import Operations

# pypi packages
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

bot = commands.Bot(command_prefix="!")
token = Keys.get_key(Keys.token)

# globals
GUILD_ID = Keys.get_key(Keys.guild_id)
AVAILABLE_SOUND_EFFECTS = [file.split('.')[0].upper() for file in os.listdir('./sound_effects')]
CURRENT_VOICE_CLIENT = None


# sync functions


def return_valid_message(msg_str: str):
    if len(msg_str) <= 1:
        raise NotLongEnough(msg_str)
    if msg_str[0] == '!':
        msg_str = msg_str[:1]
    return msg_str.upper().strip()

# bot events


@bot.event
async def on_ready():
    msg = f'Connected to {bot.get_guild(int(GUILD_ID))}.'
    logger.info(msg)


@bot.event
async def on_message(message) -> None:  # currently only plays sound effects
    author = message.author
    if author == bot.user:  # move to everwhere but 'elif msg_str in available sounds'
        return None

    channel_type_str = str(message.channel.type)
    msg_str = str(message.content)
    logger.debug(f'{author} sent a message aimed at a {channel_type_str} channel')

    # decipher commands.py being made

    if channel_type_str == "private":
        try:
            msg_str = return_valid_message(msg_str)
            if msg_str in ['JOIN', 'CONNECT']:
                logger.info(f'{author} requested bot to join {bot.get_guild(int(GUILD_ID))}')
                await join_vc(message)

            elif msg_str in ['LEAVE', 'DISCONNECT']:
                await leave_vc(message)

            elif msg_str in AVAILABLE_SOUND_EFFECTS:
                # get channel user is in and join
                voice = await join_vc(message)

                if not voice or isinstance(voice, str):
                    message.author.send("\n".join([ExceptionStrings.to_user, voice]))
                    return None

                # send message
                await message.author.send(f'Playing {message.content}')

                # play music
                source = FFmpegPCMAudio(f'./sound_effects/{msg_str}.mp3')
                sound_player = voice.play(source)

                # leave channel
                await leave_vc(message)

            elif msg_str in ['HELP', 'HELP ME']:
                help_message = 'Send me a message of the sound effect you\'d like me to play.\n' \
                               'Available sound effects:\n' \
                               f'{AVAILABLE_SOUND_EFFECTS}'
                await message.author.send(help_message)
            else:
                logger.debug(msg_str)
                unknown_cmd_message = f'Not sure I understand what you\'re saying. Type \'help\' for a list of commands.'
                logger.debug('Sent unkown command message')
                await message.author.send(unknown_cmd_message)

        except (NotLongEnough, NoneType) as e:
            logger.exception(e.for_user())
            await message.author.send(e.for_user())

        except Exception as e:
            logger.exception(f'{ExceptionStrings.to_console} {e}')
            await message.author.send(ExceptionStrings.to_user_on_message)


bot.run(token)
