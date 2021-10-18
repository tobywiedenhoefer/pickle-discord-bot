# base packages
import os
from typing import Union

# local packages
from logger import logger
from APIKeys import Keys
from Exceptions import ExceptionStrings
from Exceptions import NotLongEnough, NoneType
from commands import Command

# pypi packages
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
token = Keys.get_key(Keys.token)

# globals
GUILD_ID = Keys.get_key(Keys.guild_id)

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
    logger.info(f'{author} sent a message aimed at a {channel_type_str} channel')

    if channel_type_str == "private":
        cmd = Command(message=message, bot=bot, vc=None)
        try:
            # execute command
            await cmd.exec()
        except (NotLongEnough, NoneType) as e:
            logger.exception(e.for_user())
            await message.author.send(e.for_user())
        except Exception as e:
            logger.exception(f'{ExceptionStrings.to_console} {e}')
            logger.exception(f'Error occurred after user sent: {msg_str}')
            await message.author.send(ExceptionStrings.to_user_on_message)


bot.run(token)
