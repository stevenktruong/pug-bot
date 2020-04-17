from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(have_no_pug, invalid_number_multiple)
async def remove(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    arguments = set(user_input["arguments"].split())

    for player_num_string in arguments:
        player_num = int(player_num_string)

        # If the number is not in the correct range
        if not 1 <= player_num <= len(owned_pug.players):
            return await message.channel.send(INVALID_NUMBER)

    for player_num_string in arguments:
        player_num = int(player_num_string)
        owned_pug.remove_player(owned_pug.players[player_num-1])

    await update_status(message.channel, owned_pug)