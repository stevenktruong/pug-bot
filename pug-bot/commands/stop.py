from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *
    
@check(have_no_pug, pug_already_stopped)
async def stop(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)

    # Pick a channel to move players into
    channels = [channel for channel in message.guild.voice_channels]
    await message.channel.send(PICK_A_CHANNEL)

    # Wait for input
    result = await client.wait_for("message", check=lambda m: m.author == message.author)
    try:
        index = int(result.content)-1
    except:
        await message.channel.send(DONT_MOVE_PLAYERS)
    else:
        if not 0 <= index < len(channels):
            await message.channel.send(DONT_MOVE_PLAYERS)
        for player in owned_pug.players:
            await player.move_to(channels[index])

    # Report winner
    team_message = f"{REPORT_WINNER}\n"
    for (i, team) in enumerate(owned_pug.teams):
        team_message += f"`[{i+1}]` Team {team.name}\n"
    await message.channel.send(team_message)

    result = await client.wait_for("message", check=lambda m: m.author == message.author)
    try:
        index = int(result.content)-1
    except:
        await message.channel.send(NO_WINNER)
    else:
        if not 0 <= index < len(owned_pug.teams):
            await message.channel.send(NO_WINNER)
        owned_pug.teams[index].wins += 1

    # Stop pug
    owned_pug.active = 0
    await update_status(message.channel, owned_pug)