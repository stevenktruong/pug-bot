import time

from .checks import *

from ..config import *
from ..pug import Pug
from ..utils import *

@check(input_too_long, already_have_pug)
async def create(message, pugs, user_input, client):
    size_string = user_input["arguments"].split().pop()

    # Scrape the desired PUG size
    try:
        pug_size = int(size_string)
    except:
        return await message.channel.send(NO_PUG_SIZE)

    if not 0 < pug_size <= 100:
        return await message.channel.send(TEAM_SIZE_RANGE)

    # Remove the numbers and the space right before the numbers
    pug_name = user_input["arguments"][0:-(len(size_string)+1)]

    # Check if a PUG with the desired name exists
    existing_pug = find_in_list(lambda pug: pug.name == pug_name, pugs)
    if existing_pug:
        return await message.channel.send(PUG_ALREADY_EXISTS)

    # Check if the input included a PUG name
    if not pug_name:
        return await message.channel.send(NO_PUG_NAME)

    # Create the pug
    new_pug = Pug(name=pug_name, owner=message.author, max_size=pug_size, last_action=time.time(), teams=[], players=[], active=0)
    pugs.add(new_pug)

    # Send the pug status embed
    await update_status(message.channel, new_pug)