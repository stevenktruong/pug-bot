from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(have_no_pug)
async def remove(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)

    # Attempt to cast the argument as an int
    try:
        player_num = int(user_input["arguments"])
    except:
        await message.channel.send(INVALID_NUMBER)
        return

    # If the number is not in the correct range
    if not 1 <= player_num <= len(owned_pug.players):
        await message.channel.send(INVALID_NUMBER)
        return

    # Remove the player from the PUG
    owned_pug.remove_player(owned_pug.players[player_num-1])
    await update_status(message.channel, owned_pug)