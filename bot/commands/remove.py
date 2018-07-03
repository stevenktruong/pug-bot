from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(have_no_pug, invalid_number)
async def remove(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    player_num = int(user_input["arguments"])

    # If the number is not in the correct range
    if not 1 <= player_num <= len(owned_pug.players):
        return await message.channel.send(INVALID_NUMBER)

    # Remove the player from the PUG
    owned_pug.remove_player(owned_pug.players[player_num-1])
    await update_status(message.channel, owned_pug)