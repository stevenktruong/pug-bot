from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(not_in_pug, not_a_captain, invalid_number)
async def kick(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    player_num = int(user_input["arguments"])

    # Kick the team member
    current_team = existing_pug.find_team(message.author)
    if not 1 <= player_num <= len(current_team.members):
        return await message.channel.send(INVALID_NUMBER)

    existing_pug.remove_from_team(message.author, player_num)
    await update_status(message.channel, existing_pug)