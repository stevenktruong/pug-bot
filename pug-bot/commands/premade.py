from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(not_in_pug, invalid_number_multiple)
async def premade(message, pugs, user_input, client):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    arguments = list(user_input["arguments"].split())

    for player_num_string in arguments:
        player_num = int(player_num_string)

        # If the number is not in the correct range or if the chosen player is on a team already
        if not 1 <= player_num <= len(existing_pug.players) or existing_pug.find_team(existing_pug.players[player_num-1]):
            return await message.channel.send(INVALID_PICK)
    
    # The first listed player becomes the captain
    captain_num = int(arguments[0])
    captain = existing_pug.players[captain_num-1]
    existing_pug.add_team(captain)

    for player_num_string in arguments[1:]:
        player_num = int(player_num_string)
        existing_pug.add_to_team(captain, player_num)

    await update_status(message.channel, existing_pug)