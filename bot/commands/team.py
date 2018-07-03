from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(input_too_long, not_in_pug, team_already_exists, already_in_team)
async def team(message, pugs, user_input, client):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    team_name = user_input["arguments"]

    existing_pug.add_team(message.author, team_name)
    await update_status(message.channel, existing_pug)