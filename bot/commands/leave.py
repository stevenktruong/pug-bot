from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *    
    
@check(not_in_pug)
async def leave(message, pugs, user_input, client):
    existing_pug.remove_player(message.author)
    await update_status(message.channel, existing_pug)