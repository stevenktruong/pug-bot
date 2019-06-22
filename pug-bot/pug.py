from .team import Team
from .utils import find_in_list


class Pug:

    def __init__(self, name, owner, max_size, last_action, teams=[], players=[], channel=None, status=None, active=0):
        """
        `teams` is a dictionary of the following shape:
            {
                name1: [ team members ], (first element is the captain)
                name2: [ team members ]
            }

        `players` is a list of all participating players
        `status` is a reference to some outside status message
        Values of `active`:
            0    Stopped pug
            1    Active pug
            2    Closed pug
        """
        self.name = name
        self.owner = owner
        self.max_size = max_size
        self.last_action = last_action
        self.teams = teams
        self.players = players
        self.channel = channel
        self.status = status
        self.active = active

    def add_team(self, captain, name=None):
        if not captain in self.players:
            raise ValueError("That person is not a player")
        if name in map(lambda team: team.name, self.teams):
            raise ValueError("That team name already exists")

        if not name:
            # Defaults to 1, 2, etc.
            name = str(len(self.teams)+1)

        self.teams.append(Team(name, [captain]))

    def add_to_team(self, captain, player_num):
        """
        `player_num` is the number in the visible list. E.g., if you want to add the first player,
        you'll set `player_num=1` instead of `player_num=0`.
        """
        if not self.is_captain(captain):
            raise ValueError("The passed captain is not a captain")
        if not player_num-1 in range(len(self.players)):
            raise ValueError(f"{player_num} is not a valid number")
        if self.find_team(self.players[player_num-1]):
            raise ValueError("That player is already in a team")

        self.find_team(captain).add_member(self.players[player_num-1])

    def remove_from_team(self, captain, player_num):
        """
        See `add_to_team` for the number convention
        """
        current_team = self.find_team(captain)
        if not current_team:
            raise ValueError("The passed captain is not in a team")
        if not self.is_captain(captain):
            raise ValueError("The passed captain is not a captain")
        if not player_num-1 in range(len(current_team.members)):
            raise ValueError(f"{player_num} is not a valid number")

        current_team.remove_member(current_team.members[player_num-1])

        # If the team is empty after removing a player, delete the team
        if not current_team.members:
            self.teams.remove(current_team)
            del current_team

    def add_player(self, player):
        if len(self.players) < self.max_size:
            self.players.append(player)
            return True
        else:
            return False

    def remove_player(self, player):
        if not player in self.players:
            raise ValueError("That person is not in the PUG.")

        self.players.remove(player)

        # Remove the player from any lists
        current_team = find_in_list(
            lambda team: player in team.members, self.teams)
        if current_team:
            current_team.remove_member(player)

            # If the team is empty after removing a player, delete the team
            if not current_team.members:
                self.teams.remove(current_team)
                del current_team

    def is_captain(self, player):
        return player in map(lambda team: team.members[0], self.teams)

    def find_team(self, player):
        current_team = find_in_list(
            lambda team: player in team.members, self.teams)
        if current_team:
            return current_team
        else:
            return None

    def remaining_players(self):
        """
        If a player has already been chosen, then its number will be negative.
        E.g., if the second player has been chosen, this returns (-2, player).
        """

        for (i, player) in enumerate(self.players):
            if not self.find_team(player):
                yield (i+1, player)
            else:
                yield (-(i+1), player)
