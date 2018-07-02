from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *
    
@check(have_no_pug)
async def stop(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)

    # Pick a channel to move players into
    channels = [channel for channel in message.guild.voice_channels]
    await message.channel.send(PICK_A_CHANNEL_END)

    # Wait for input
    result = await client.wait_for("message", check=lambda m: m.author == message.author)
    try:
        index = int(result.content)-1
    except:
        await message.channel.send(DONT_MOVE_PLAYERS)
        return
    else:
        for player in owned_pug.players:
            await player.move_to(channels[index])

    # Stop pug
    owned_pug.active = 0
    await update_status(message.channel, owned_pug)