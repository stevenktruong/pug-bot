from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(not_in_pug, not_a_captain, invalid_number)
async def channel(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    index = int(user_input["arguments"])-1

    # Check if the channel has been taken
    # If at least one team channel has picked that channel
    channels = [channel for channel in message.guild.voice_channels]

    if not 1 <= index <= len(channels):
        await message.channel.send(INVALID_NUMBER)
        return

    if not all(not team.channel == channels[index] for team in existing_pug.teams):
        await message.channel.send(CHANNEL_ALREADY_PICKED)
        return

    # Pick the channel
    existing_pug.find_team(message.author).channel = channels[index]
    await update_status(message.channel, existing_pug)