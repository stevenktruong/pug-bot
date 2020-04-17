from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(not_in_pug, not_a_captain, invalid_number_multiple)
async def kick(message, pugs, user_input, client):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    arguments = set(user_input["arguments"].split())

    for player_num_string in arguments:
        player_num = int(player_num_string)

        # Kick the team member
        current_team = existing_pug.find_team(message.author)
        if not 1 <= player_num <= len(current_team.members):
            return await message.channel.send(INVALID_NUMBER)

    for player_num_string in arguments:
        player_num = int(player_num_string)
        existing_pug.remove_from_team(message.author, player_num)
    
    await update_status(message.channel, existing_pug)