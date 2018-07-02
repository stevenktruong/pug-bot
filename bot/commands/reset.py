from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(have_no_pug)
async def reset(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
    
    # Erase teams
    owned_pug.teams = []
    await update_status(message.channel, owned_pug)