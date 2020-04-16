import discord

from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

async def help(message, username):
    help_embed = discord.Embed(
        title=TITLE,
        description=DESCRIPTION,
        type="rich",
        color=discord.Color.blue()
    )

    help_embed.set_author(name=username)

    help_embed.add_field(
        name=HOW_TO_USE,
        value=USE_MESSAGE
    )

    help_embed.add_field(
        name=COMMANDS,
        value=COMMANDS_MESSAGE,
        inline=False
    )

    help_embed.add_field(
        name=ADD,
        value=ADD_MESSAGE,
        inline=False
    )

    help_embed.set_footer(
        text=FOOTER_TEXT,
        icon_url=FOOTER_ICON
    )

    await message.author.send(embed=help_embed)