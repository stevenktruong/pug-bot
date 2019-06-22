from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(not_in_pug, not_a_captain, invalid_number)
async def pick(message, pugs, user_input, client):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    player_num = int(user_input["arguments"])

    # If the number is not in the correct range or if the chosen player is on a team already
    if not 1 <= player_num <= len(existing_pug.players) or existing_pug.find_team(existing_pug.players[player_num-1]):
        return await message.channel.send(INVALID_PICK)

    # Add player to team
    existing_pug.add_to_team(message.author, player_num)
    await update_status(message.channel, existing_pug)