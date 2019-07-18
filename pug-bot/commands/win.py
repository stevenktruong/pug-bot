from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *
    
@check(have_no_pug, pug_already_stopped, invalid_number)
async def win(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    team_num = int(user_input["arguments"])

    # If the number is not in the correct range
    if not 1 <= team_num <= len(owned_pug.teams):
        return await message.channel.send(INVALID_NUMBER)

    # Update wins
    owned_pug.teams[team_num-1].wins += 1
    await update_status(message.channel, owned_pug)