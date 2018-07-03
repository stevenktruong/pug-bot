from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *    
    
@check(not_in_pug)
async def leave(message, pugs, user_input, client):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    existing_pug.remove_player(message.author)
    await update_status(message.channel, existing_pug)