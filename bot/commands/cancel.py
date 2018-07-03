from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(have_no_pug)
async def cancel(message, pugs, user_input, client):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)

    # Delete the status message if it exists
    if owned_pug.status:
        await owned_pug.status.delete()

    # Remove reference to the pug
    pugs.remove(owned_pug)
    await message.channel.send(DELETED_PUG)