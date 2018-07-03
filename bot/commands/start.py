from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(have_no_pug, pug_has_no_teams, channels_not_picked)
async def start(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)

    # Move the team members to their channel
    for team in owned_pug.teams:
        for member in team.members:
            await member.move_to(team.channel)

    owned_pug.active = 1
    await update_status(message.channel, owned_pug)