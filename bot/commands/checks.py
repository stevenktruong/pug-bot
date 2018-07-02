from ..config import *
from ..utils import find_in_list

# The first parameters of commands should be
#    message, pugs
# in that order.

def check(*args):
    """
    `args` should be a list of functions
    """
    def wrapper(function):
        # This is the function to replace the decorated function
        async def wrapped(message, pugs, user_input):
            for error in [check(message, pugs, user_input) for check in args]:
                if not error == None:
                    return await message.channel.send(error)
            await function(message, pugs, user_input)
        return wrapped
    return wrapper


def input_too_long(message, pugs, user_input):
    if len(message.content) > 100:
        return INPUT_TOO_LONG

def already_have_pug(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
    if owned_pug:
        return ALREADY_HAVE_PUG

def have_no_pug(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
    if not owned_pug:
        return HAVE_NO_PUG

def already_in_pug(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if existing_pug:
        return ALREADY_IN_PUG

def not_in_pug(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if not existing_pug:
        return NOT_IN_PUG

def pug_doesnt_exist(message, pugs, user_input):
    pug_name = user_input["arguments"]
    existing_pug = find_in_list(lambda pug: pug.name == pug_name, pugs)
    if not existing_pug:
        return PUG_DOESNT_EXIST

def pug_has_no_teams(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
    if not owned_pug.teams:
        return PUG_HAS_NO_TEAMS

def channels_not_picked(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
    if not all(team.channel for team in owned_pug.teams):
        return CHANNELS_NOT_PICKED

def invalid_number(message, pugs, user_input):
    arguments = user_input["arguments"].split()
    # Attempt to cast the input as an int
    try:
        int(arguments[-1])
    except:
        return INVALID_NUMBER

# You need to check `invalid_number` before checking this
def not_enough_players(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
    arguments = user_input["arguments"].split()

    # If there would be more teams than players
    if int(arguments[-1]) > len(owned_pug.players):
        return NOT_ENOUGH_PLAYERS

# You need to check `invalid_number` before checking this
def non_negative_number(message, pugs, user_input):
    arguments = user_input["arguments"].split()

    # If there would be more teams than players
    if int(arguments[-1]) <= 0:
        return NON_NEGATIVE_NUMBER

# You need to check `not_in_pug` before checking this
def team_already_exists(message, pugs, user_input):
    team_name = user_input["arguments"]
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if team_name in map(lambda team: team.name, existing_pug.teams):
        return TEAM_ALREADY_EXISTS

# You need to check `not_in_pug` before checking this
def already_in_team(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if existing_pug.find_team(message.author):
        return ALREADY_IN_TEAM

# You need to check `not_in_pug` before checking this
def not_a_captain(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if not existing_pug.is_captain(message.author):
        return NOT_A_CAPTAIN