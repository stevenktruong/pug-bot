from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(already_in_pug, pug_doesnt_exist)
async def join(message, pugs, user_input, client):
    pug_name = user_input["arguments"]
    current_pug = find_in_list(lambda pug: pug.name == pug_name, pugs)

    # Attempt to add the user to the PUG and check for success
    if not current_pug.add_player(message.author):
        return await message.channel.send(PUG_IS_FULL)

    await update_status(message.channel, current_pug)