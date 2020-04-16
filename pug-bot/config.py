# Bot Configuration
prefix = ".."

# Messages
# Help messages
TITLE = "🤖 `pug-bot` (Pick-up Bot)"
DESCRIPTION = "I'm a bot for managing pick-up games (aka a scrim)."
HOW_TO_USE = "🤔 How to Use Me"
COMMANDS = "⌨️ Available Commands"
FOOTER_TEXT = "https://github.com/stevenktruong/pug-bot"
FOOTER_ICON = "https://camo.githubusercontent.com/7710b43d0476b6f6d4b4b2865e35c108f69991f3/68747470733a2f2f7777772e69636f6e66696e6465722e636f6d2f646174612f69636f6e732f6f637469636f6e732f313032342f6d61726b2d6769746875622d3235362e706e67"

USE_MESSAGE = ""
USE_MESSAGE += f"1. `{prefix}create` a PUG.\n"
USE_MESSAGE += f"2. `{prefix}join` your PUG and have your friends `{prefix}join` it, too.\n"
USE_MESSAGE += f"3. Create teams and have captains `{prefix}pick` teammates.\n"
USE_MESSAGE += f"4. Have captains pick voice channels, and then `{prefix}start`!\n"
USE_MESSAGE += f"5. After you're done playing, you can `{prefix}stop` the PUG.\n"
USE_MESSAGE += f"6. When you're done with the lobby, you can `{prefix}close` it.\n"
USE_MESSAGE += "\u200b"

COMMANDS_MESSAGE = ""
COMMANDS_MESSAGE += f"**{prefix}create [name] [size]** - Create a PUG\n"
COMMANDS_MESSAGE += f"**{prefix}owner [number]** - Change the PUG owner\n"
COMMANDS_MESSAGE += f"**{prefix}join [name]** - Join the listed PUG\n"
COMMANDS_MESSAGE += f"**{prefix}leave** - Leave your PUG\n"
COMMANDS_MESSAGE += f"**{prefix}cancel** - Delete the PUG you created\n"
COMMANDS_MESSAGE += f"**{prefix}start** - Starts your PUG and moves teams to their channels\n"
COMMANDS_MESSAGE += f"**{prefix}stop** - Stops the PUG and move players to a channel\n"
COMMANDS_MESSAGE += f"**{prefix}close** - Close a PUG\n"
COMMANDS_MESSAGE += f"**{prefix}reset** - Reset a PUG\n"
COMMANDS_MESSAGE += f"**{prefix}refresh** - Show the PUG status\n"
COMMANDS_MESSAGE += f"**{prefix}remove [number]** - Remove a player from the PUG\n"
COMMANDS_MESSAGE += f"**{prefix}random [teams]** - Randomly create teams in your PUG, if possible\n"
COMMANDS_MESSAGE += f"**{prefix}random captains [teams]** - Randomly assign captains in your PUG, if possible\n"
COMMANDS_MESSAGE += f"**{prefix}team [team name]** - Create a team with the listed name\n"
COMMANDS_MESSAGE += f"**{prefix}captain [number]** - Make one of your teammates a captain\n"
COMMANDS_MESSAGE += f"**{prefix}rename [team name]** - Rename your team\n"
COMMANDS_MESSAGE += f"**{prefix}pick [number]** - Pick teammates\n"
COMMANDS_MESSAGE += f"**{prefix}kick [number]** - Kick teammates from your team\n"
COMMANDS_MESSAGE += f"**{prefix}channel [number]** - Select your team's voice channel\n"
COMMANDS_MESSAGE += f"**{prefix}win [number]** - Add a win to a team\n"
COMMANDS_MESSAGE += f"**{prefix}roll [number] [number]** - Randomly pick a number\n"
COMMANDS_MESSAGE += "\u200b"

# Commands
PICK_A_CHANNEL = "Pick a channel to move all players into. (Type anything else to not move players)"
REPORT_WINNER = "Report the winning team. (Type anything else to not report)"

# Success messages
NO_WINNER = "Didn't change the wins count."
DELETED_PUG = "Successfully deleted the PUG."
DONT_MOVE_PLAYERS = "Did not move players."
def ROLLED(number):
    return f"Rolled {number}."

# Input errors
INPUT_TOO_LONG = "The input is too long. Try something shorter."
NO_PUG_NAME = "I couldn't find a PUG name. Please try again."
TEAM_SIZE_RANGE = "A team size must lie between 1 and 100. Please try again."
INVALID_NUMBER = "That wasn't a valid number. Please try again."
NON_NEGATIVE_NUMBER = "The number must be positive. Please try again."
INVALID_RANGE = "That wasn't a valid range of numbers. Please try again."

# PUG errors
ALREADY_HAVE_PUG = "You already have an active PUG."
HAVE_NO_PUG = "You don't have any PUGs."
NO_PUG_SIZE = "I couldn't find a PUG size."
PUG_ALREADY_EXISTS = "A PUG with that name already exists. Please try a different name."
ALREADY_IN_PUG = "You're already in a PUG."
NOT_IN_PUG = "You're not currently in any PUG."
PUG_DOESNT_EXIST = "That PUG doesn't exist."
PUG_IS_FULL = "That PUG is full."
PUG_HAS_NO_TEAMS = "There are no teams in the PUG."
PUG_ALREADY_STARTED = "The PUG has already started."
PUG_ALREADY_STOPPED = "The PUG has already stopped."

# Team errors
NOT_ENOUGH_PLAYERS = "There aren't enough people for that many teams. Please try again."
TEAM_ALREADY_EXISTS = "A team with that name already exists."
ALREADY_IN_TEAM = "You're already in a team."
INVALID_PICK = "That wasn't a valid pick. Try again."

# Channel errors
CHANNEL_ALREADY_PICKED = "That channel has been taken already. Try again."
CHANNELS_NOT_PICKED = "Not all teams have chosen their channel yet."

# Permission errors
NOT_A_CAPTAIN = "Only captains can do that."
