# base packages
import os

# local packages
from APIKeys import Keys, get_key
from Exceptions import ExceptionStrings
from Exceptions import NotLongEnough, NoneType
from operations import Operations

# pypi packages
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

bot = commands.Bot(command_prefix="!")
token = get_key(Keys.token)

# globals
GUILD_ID = get_key(Keys.guild_id)
AVAILABLE_SOUND_EFFECTS = [file.split('.')[0].upper() for file in os.listdir('./sound_effects')]
CURRENT_VOICE_CLIENT = None


# sync functions


def return_valid_message(msg_str: str):
    if len(msg_str) <= 1:
        raise NotLongEnough(msg_str)
    if msg_str[0] == '!':
        msg_str = msg_str[:1]
    return msg_str.upper().strip()


def get_guild_object():
    return bot.get_guild(int(GUILD_ID))


# async methods


async def join_vc(message: discord.Message):
    global CURRENT_VOICE_CLIENT
    # exit immediately if the most recent voice client is connected:
    if CURRENT_VOICE_CLIENT and CURRENT_VOICE_CLIENT.is_connected():
        return CURRENT_VOICE_CLIENT

    await message.author.send('Joining voice chat...')

    # get channel user is in and join
    guild = get_guild_object()

    try:
        if not guild:
            raise NoneType(Operations.connect_to_guild, 'guild', None)
        member = await guild.fetch_member(message.author.id)
        channel = member.voice.channel

        CURRENT_VOICE_CLIENT = await channel.connect()
        await message.author.send('Successfully connected!')
        return CURRENT_VOICE_CLIENT

    except (NoneType) as e:
        return e.for_user()
    except Exception as e:
        return e


async def leave_vc(message: discord.Message):
    if CURRENT_VOICE_CLIENT and CURRENT_VOICE_CLIENT.is_connected():
        guild = get_guild_object()
        await guild.voice_client.disconnect()
        await message.author.send('I left the voice chat.')


# bot events


@bot.event
async def on_ready():
    print(f'Connected to {bot.get_guild(int(GUILD_ID))}.')


@bot.event
async def on_message(message):  # currently only plays sound effects
    channel_type_str = str(message.channel.type)
    msg_str = str(message.content)

    if channel_type_str == "private":
        try:
            msg_str = return_valid_message(msg_str)
            if msg_str in ['JOIN', 'CONNECT']:
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
                print('Message: ', msg_str)
                unknown_cmd_message = f'Not sure I understand what you\'re saying. Type \'help\' for a list of commands.'
                print(unknown_cmd_message)
                await message.author.send(unknown_cmd_message)

        except (NotLongEnough, NoneType) as e:
            print(e.for_user())
            await message.author.send(e.for_user())

        except Exception as e:
            print(ExceptionStrings.to_console, e)
            await message.author.send(ExceptionStrings.to_user_on_message)


bot.run(token)
