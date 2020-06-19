from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(have_no_pug)
async def close(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)

    # Close the pug
    await update_status(message.channel, owned_pug, PUG_ENDED)

    # Remove the reference to the pug
    pugs.remove(owned_pug)