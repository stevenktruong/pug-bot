from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(not_in_pug, not_a_captain, invalid_number)
async def captain(message, pugs, user_input, client):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    player_num = int(user_input["arguments"])

    # Check if the number is in the correct range
    current_team = existing_pug.find_team(message.author)
    if not 1 <= player_num <= len(current_team.members):
        return await message.channel.send(INVALID_NUMBER)

    # Change the team captain
    current_team.members.insert(0, current_team.members.pop(player_num-1))
    await update_status(message.channel, existing_pug)