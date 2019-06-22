from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(not_in_pug, not_a_captain, invalid_number)
async def channel(message, pugs, user_input, client):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    index = int(user_input["arguments"].split().pop())-1

    # Check if the channel has been taken
    channels = [channel for channel in message.guild.voice_channels]

    # These checks are part of the logic of picking a channel, so they are kept here
    if not 1 <= index+1 <= len(channels):
        return await message.channel.send(INVALID_NUMBER)

    # If at least one team channel has picked that channel
    if channels[index] in [team.channel for team in existing_pug.teams]:
        return await message.channel.send(CHANNEL_ALREADY_PICKED)

    # Pick the channel
    existing_pug.find_team(message.author).channel = channels[index]
    await update_status(message.channel, existing_pug)