import discord
import asyncio
from random import shuffle, randint
import re
import os

from pug import Pug
from team import Team

from utils import *
from config import *

# Get the token from environment variables. Otherwise, get it from the config
TOKEN = os.getenv('TOKEN') if os.getenv('TOKEN') else TOKEN

# guild_list is of the form
# {
#     guild: set()
# }
guild_list = {}

client = discord.Client()

@client.event
async def on_ready():
    print("Successfully logged in.")
    print(f"Username: {client.user.name}")
    print(f"ID: {client.user.id}")

@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    user_input = {"command": ""}
    if message.content.startswith(f"{prefix}"):
        user_input = parse_command(message.content)

    ########################################
    #### Help function
    ########################################
    if user_input["command"] == "help":
        help_embed = discord.Embed(
            title=TITLE,
            description=DESCRIPTION,
            type="rich",
            color=discord.Color.blue()
        )

        help_embed.set_author(name=client.user.name)

        help_embed.add_field(
            name=HOW_TO_USE,
            value=USE_MESSAGE
        )

        help_embed.add_field(
            name=COMMANDS,
            value=COMMANDS_MESSAGE,
            inline=False
        )

        help_embed.set_footer(
            text=FOOTER_TEXT,
            icon_url=FOOTER_ICON
        )

        await message.author.send(embed=help_embed)

    # Add the guild to the guilds list if it's not in it already
    if not message.guild.name in guild_list.keys():
        guild_list[message.guild.name] = set()

    pugs = guild_list[message.guild.name]

    ########################################
    #### Creating a pug
    ########################################
    if user_input["command"] == "create":
        # Check if input is too long
        if len(message.content) > 100:
            await message.channel.send(INPUT_TOO_LONG)
            return

        # Check if a user already has a PUG or not
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if owned_pug:
            await message.channel.send(ALREADY_HAVE_PUG)
            return

        size_string = user_input["arguments"].split().pop()

        # Scrape the desired PUG size
        try:
            pug_size = int(size_string)
        except:
            await message.channel.send(NO_TEAM_SIZE)
            return

        if not 0 < pug_size <= 100:
            await message.channel.send(TEAM_SIZE_RANGE)
            return

        # Remove the numbers and the space right before the numbers
        pug_name = user_input["arguments"][0:-(len(size_string)+1)]

        # Check if a PUG with the desired name exists
        existing_pug = find_in_list(lambda pug: pug.name == pug_name, pugs)
        if existing_pug:
            await message.channel.send(PUG_ALREADY_EXISTS)
            return

        # Check if the input included a PUG name
        if not pug_name:
            await message.channel.send(NO_PUG_NAME)
            return

        # Create the pug
        new_pug = Pug(name=pug_name, creator=message.author, max_size=pug_size, teams=[], players=[], active=0)
        pugs.add(new_pug)

        # Send the pug status embed
        await update_status(message.channel, new_pug)


    ########################################
    #### Joining a pug
    ########################################
    if user_input["command"] == "join":
        pug_name = user_input["arguments"]
        
        # Check if a user is already in a PUG
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if existing_pug:
            await message.channel.send(ALREADY_IN_PUG)
            return

        current_pug = find_in_list(lambda pug: pug.name == pug_name, pugs)
        if not current_pug:
            await message.channel.send(PUG_DOESNT_EXIST)
            return

        # Attempt to add the user to the PUG and check for success
        if not current_pug.add_player(message.author):
            await message.channel.send(PUG_IS_FULL)
            return

        await update_status(message.channel, current_pug)


    ########################################
    #### Leaving a pug
    ########################################
    if user_input["command"] == "leave":
        # Check if a user is in a PUG
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if not existing_pug:
            await message.channel.send(NOT_IN_PUG)
            return

        # Leave the pug
        existing_pug.remove_player(message.author)
        await update_status(message.channel, existing_pug)


    ########################################
    #### Cancelling a pug
    ########################################
    if user_input["command"] == "cancel":
        # Check if the user owns a pug
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if not owned_pug:
            await message.channel.send(HAVE_NO_PUG)
            return

        await message.channel.send(DELETED_PUG)

        if owned_pug.status:
            await owned_pug.status.delete()

        # Remove reference to the pug
        pugs.remove(owned_pug)


    #########################################
    #### Starting a pug
    ########################################
    if user_input["command"] == "start":
        # Check if the user owns a pug
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if not owned_pug:
            await message.channel.send(HAVE_NO_PUG)
            return

        if not owned_pug.teams:
            await message.channel.send(PUG_HAS_NO_TEAMS)
            return

        if not all(team.channel for team in owned_pug.teams):
            await message.channel.send(CHANNELS_NOT_PICKED)
            return

        # Move the team members to their channel
        for team in owned_pug.teams:
            for member in team.members:
                await member.move_to(team.channel)

        owned_pug.active = 1
        await update_status(message.channel, owned_pug)

    #########################################
    #### Stopping a pug
    ########################################
    if user_input["command"] == "stop":
        # Check if the user owns a pug
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if not owned_pug:
            await message.channel.send(HAVE_NO_PUG)
            return

        if not owned_pug.teams:
            await message.channel.send(PUG_HAS_NO_TEAMS)
            return

        if not all(team.channel for team in owned_pug.teams):
            await message.channel.send(CHANNELS_NOT_PICKED)
            return

        # Pick a channel to move players into
        channels = [channel for channel in message.guild.voice_channels]

        channel_message = f"{PICK_A_CHANNEL_END}\n\u200b\n" # '\u200b' gives an empty line
        for (i, channel) in enumerate(channels):
            channel_message += f"`[{i+1}]` {channel}\n"
        channel_list = await message.channel.send(channel_message)

        # Wait for input
        result = await client.wait_for("message", check=lambda m: m.author == message.author)
        try:
            index = int(result.content)-1
        except:
            await message.channel.send(DONT_MOVE_PLAYERS)
            return
        else:
            for player in owned_pug.players:
                await player.move_to(channels[index])

        # Stop pug
        owned_pug.active = 0
        await update_status(message.channel, owned_pug)


    ########################################
    #### Close a pug
    ########################################
    if user_input["command"] == "close":
        # Check if the user owns a pug
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if not owned_pug:
            await message.channel.send(HAVE_NO_PUG)
            return

        # Close the pug
        owned_pug.active = 2
        await update_status(message.channel, owned_pug)

        # Remove the reference to the pug
        pugs.remove(owned_pug)


    ########################################
    #### Resetting a pug
    ########################################
    if user_input["command"] == "reset":
        # Check if the user owns a pug
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if not owned_pug:
            await message.channel.send(HAVE_NO_PUG)
            return

        # Erase teams
        owned_pug.teams = []
        await update_status(message.channel, owned_pug)


    ########################################
    #### Refreshing the message
    ########################################
    if user_input["command"] == "refresh":
        # Check if the user is in a pug
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if not existing_pug:
            await message.channel.send(HAVE_NO_PUG)
            return

        # Refresh the message
        await update_status(message.channel, existing_pug)


    ########################################
    #### Remove a player
    ########################################
    if user_input["command"] == "remove":
        # Check if the user owns a pug
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if not owned_pug:
            await message.channel.send(HAVE_NO_PUG)
            return

        # Attempt to cast the argument as an int
        try:
            player_num = int(user_input["arguments"])
        except:
            await message.channel.send(INVALID_NUMBER)
            return

        # If the number is not in the correct range
        if not 1 <= player_num <= len(owned_pug.players):
            await message.channel.send(INVALID_NUMBER)
            return

        # Remove the player from the PUG
        owned_pug.remove_player(owned_pug.players[player_num-1])
        await update_status(message.channel, owned_pug)


    ########################################
    #### Randomize teams
    ########################################
    if user_input["command"] == "random":
        # Check if the user owns a pug
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if not owned_pug:
            await message.channel.send(HAVE_NO_PUG)
            return

        arguments = user_input["arguments"].split()

        # Attempt to cast the input as an int
        try:
            num_teams = int(arguments[-1])
        except:
            await message.channel.send(INVALID_NUMBER)
            return

        # If there would be more teams than players
        if num_teams > len(owned_pug.players):
            await message.channel.send(NOT_ENOUGH_PLAYERS)
            return

        if num_teams <= 0:
            await message.channel.send(NON_NEGATIVE_NUMBER)
            return

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
    

    ########################################
    #### Creating a team
    ########################################
    if user_input["command"] == "team":
        # Check if input is too long
        if len(message.content) > 50:
            await message.channel.send(INPUT_TOO_LONG)
            return

        team_name = user_input["arguments"]
        
        # Check for errors
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if not existing_pug:
            await message.channel.send(NOT_IN_PUG)
            return

        if team_name in map(lambda team: team.name, existing_pug.teams):
            await message.channel.send(TEAM_ALREADY_EXISTS)
            return

        if existing_pug.find_team(message.author):
            await message.channel.send(ALREADY_IN_TEAM)
            return

        # Create the team
        existing_pug.add_team(message.author, team_name)
        await update_status(message.channel, existing_pug)


    ########################################
    #### Renaming a team
    ########################################
    if user_input["command"] == "rename":
        # Check if a user is in a pug
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if not existing_pug:
            await message.channel.send(NOT_IN_PUG)
            return

        # Check if user is a captain
        if not existing_pug.is_captain(message.author):
            await message.channel.send(NOT_A_CAPTAIN)
            return

        # If the user is a captain
        new_name = user_input["arguments"]

        # Check if the name is used somewhere else in the pug
        if not all(not team.name == new_name for team in existing_pug.teams):
            await message.channel.send(TEAM_ALREADY_EXISTS)
            return

        # Rename the team
        existing_pug.find_team(message.author).name = new_name
        await update_status(message.channel, existing_pug)


    ########################################
    #### Picking a team member
    ########################################
    if user_input["command"] == "pick":
        # Check if a user is in a pug
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if not existing_pug:
            await message.channel.send(NOT_IN_PUG)
            return

        # Check if a user is a captain
        if not existing_pug.is_captain(message.author):
            await message.channel.send(NOT_A_CAPTAIN)
            return

        try:
            player_num = int(user_input["arguments"])
        except:
            await message.channel.send(INVALID_NUMBER)
            return

        # If the number is not in the correct range or if the chosen player is on a team already
        if not 1 <= player_num <= len(existing_pug.players) or existing_pug.find_team(existing_pug.players[player_num-1]):
            await message.channel.send(INVALID_PICK)
            return

        # Add player to team
        existing_pug.add_to_team(message.author, player_num)
        await update_status(message.channel, existing_pug)


    ########################################
    #### Kicking a team member
    ########################################
    if user_input["command"] == "kick":
        # Check if a user is in a pug
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if not existing_pug:
            await message.channel.send(NOT_IN_PUG)
            return

        # Check if a user is a captain
        if not existing_pug.is_captain(message.author):
            await message.channel.send(NOT_A_CAPTAIN)
            return

        # Attempt to cast the input as an int
        try:
            player_num = int(user_input["arguments"])
        except:
            await message.channel.send(INVALID_NUMBER)
            return

        # Kick the team member
        current_team = existing_pug.find_team(message.author)
        if not 1 <= player_num <= len(current_team.members):
            await message.channel.send(INVALID_NUMBER)
            return

        existing_pug.remove_from_team(message.author, player_num)
        await update_status(message.channel, existing_pug)


    ########################################
    #### Picking a channel
    ########################################
    if user_input["command"] == "channel":
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if not existing_pug:
            await message.channel.send(NOT_IN_PUG)
            return

        if not existing_pug.is_captain(message.author):
            await message.channel.send(NOT_A_CAPTAIN)
            return

        # Find all voice channels and list them
        channels = [channel for channel in message.guild.voice_channels]

        channel_message = f"{PICK_A_CHANNEL_START}\n\u200b\n"
        for (i, channel) in enumerate(channels):
            channel_message += f"`[{i+1}]` {channel}\n"
        channel_list = await message.channel.send(channel_message)

        # Wait for input
        result = await client.wait_for("message", check=lambda m: m.author == message.author)
        try:
            index = int(result.content)-1
        except:
            await message.channel.send(INVALID_NUMBER)
            return

        # Delete the list of channels
        channel_list.delete()
        
        # Check if the channel has been taken
        # If at least one team channel has picked that channel
        if not all(not team.channel == channels[index] for team in existing_pug.teams):
            await message.channel.send(CHANNEL_ALREADY_PICKED)
            return

        # Pick the channel
        existing_pug.find_team(message.author).channel = channels[index]
        await update_status(message.channel, existing_pug)

client.run(TOKEN)