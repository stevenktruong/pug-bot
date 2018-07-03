from random import randint, shuffle

from .checks import *

from ..config import *
from ..pug import Pug
from ..team import Team
from ..utils import *

@check(have_no_pug, invalid_number, not_enough_players, non_negative_number)
async def random(message, pugs, user_input, client):
    arguments = user_input["arguments"].split()
    owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
    num_teams = int(arguments[-1])

    if len(arguments) == 1:
        # Clear teams
        owned_pug.teams = []

        # Randomize the team, including captains
        players_copy = owned_pug.players.copy()
        shuffle(players_copy)
        even_number = len(players_copy) - len(players_copy)%num_teams
        remainder = len(players_copy)%num_teams

        team_sizes = [int(even_number/num_teams)] * num_teams

        # Randomly pick the team to receive the odd people out
        for _ in range(remainder):
            team_sizes[randint(0, num_teams-1)] += 1

        # Assign the teams
        for (i, team_size) in enumerate(team_sizes):
            owned_pug.teams.append(Team(name=f"{i+1}", members=players_copy[:team_size]))
            players_copy = players_copy[team_size:]

        await update_status(message.channel, owned_pug)
    elif len(arguments) == 2 and arguments[0] == "captains":
        # Clear teams
        owned_pug.teams = []

        # Randomly pick captains
        players_copy = owned_pug.players.copy()
        shuffle(players_copy)
        for i in range(num_teams):
            owned_pug.add_team(players_copy[i])

        await update_status(message.channel, owned_pug)