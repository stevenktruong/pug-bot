from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(have_no_pug, invalid_number, non_negative_number)
async def owner(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    player_num = int(user_input["arguments"])

    # If the number is not in the correct range or if the chosen player already owns a PUG
    if not 1 <= player_num <= len(owned_pug.players) or owned_pug.players[player_num-1] in [pug.owner for pug in pugs]:
        return await message.channel.send(INVALID_NUMBER)

    # Change the owner
    owned_pug.owner = owned_pug.players[player_num-1]
    await update_status(message.channel, owned_pug)