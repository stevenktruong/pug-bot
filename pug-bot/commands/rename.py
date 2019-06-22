from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(not_in_pug, not_a_captain, team_already_exists)
async def rename(message, pugs, user_input, client):      
    existing_pug.find_team(message.author).name = new_name
    await update_status(message.channel, existing_pug)