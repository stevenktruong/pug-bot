class Team:

    def __init__(self, name, members=[], channel=None):
        # The first member is the captain
        self.name = name
        self.members = members
        self.channel = channel

    def change_captain(self, new_captain):
        if not new_captain in self.members:
            raise ValueError("The new captain must be a member of the team.")
        captain_index = self.members.index(new_captain)
        self.members.prepend(self.members.pop(captain_index))

    def add_member(self, player):
        self.members.append(player)

    def remove_member(self, player):
        if player in self.members:
            self.members.remove(player)
            