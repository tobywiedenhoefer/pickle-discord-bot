import discord
from discord.ext import commands

from commands import Command
from logger import logger
from formatter import HelpFormatter


class Play(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.token in Command._help:
          await self.help()

    async def help(self):
        formatter = HelpFormatter('Play')
        formatter.add_positional_args(
            [["{sound}", "Plays downloaded sounds."]]
        )
        formatter.add_optional_args([
            f'{",".join(Command._help)}', "show this help message and exit", ""]
        )
        await self.return_message(str(formatter))


class Sound(Play):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_args(self):
        pass
