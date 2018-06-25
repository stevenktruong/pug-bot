import discord
import asyncio
from random import shuffle, randint
import re
import os

from pug import Pug
from team import Team

from utils import *
import config

TOKEN = os.getenv('TOKEN') if os.getenv('TOKEN') else config.TOKEN

# guild_list is of the form
# {
#     guild: set()
# }
guild_list = {}

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

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
        help_message = "```"
        help_message += f"{prefix}create [pug name] [size] - Create a PUG with the given name and size.\n"
        help_message += f"{prefix}join [pug name] - Join a PUG with the given name.\n"
        help_message += f"{prefix}leave - Leave whatever PUG you're in.\n"
        help_message += f"{prefix}cancel - If you've created a PUG, this deletes it.\n"
        help_message += f"{prefix}start - If you've created a PUG, this starts it. This moves all players to the chosen channels and closes the create lobby.\n"
        help_message += f"{prefix}finish - If you've started a PUG, you can run this command to end it. Afterwards, you will no longer have access to it.\n"
        help_message += f"{prefix}random [teams] - If you own a PUG, you can randomly create as many teams as you want, if possible.\n"
        help_message += f"{prefix}random captains [teams] - If you own a PUG, you can randomly assign as many captains as you want, if possible.\n"
        help_message += f"{prefix}team [team name] - Once you're in a PUG, you can create your own team with the given name.\n"
        help_message += f"{prefix}rename [team name] - If you're a team captain, you can rename your team with this command.\n"
        help_message += f"{prefix}pick [number] - If you're team captain, you can pick your teammates with this.\n"
        help_message += f"{prefix}kick [number] - If you're team captain, you can kick your teammates with this.\n"
        help_message += f"{prefix}channel - If you're team captain, you can select a voice channel for your team. Enter the number of the voice channel you want.\n"
        help_message += "```"
        await message.author.send(help_message)


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
            await message.channel.send("The input is too long. Try something shorter.")
            return

        # Check if a user already has a PUG or not
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if owned_pug:
            await message.channel.send(f"You already have an active PUG named `{owned_pug.name}`.")
            return

        size_string = user_input["arguments"].split().pop()

        # Scrape the desired PUG size
        try:
            pug_size = int(size_string)
        except:
            await message.channel.send("I couldn't find a team size.")
            return

        if not 0 < pug_size <= 100:
            await message.channel.send("A team size must lie between 1 and 100. Please try again.")
            return

        # Remove the numbers and the space right before the numbers
        pug_name = user_input["arguments"][0:-(len(size_string)+1)]

        # Check if a PUG with the desired name exists
        existing_pug = find_in_list(lambda pug: pug.name == pug_name, pugs)
        if existing_pug:
            await message.channel.send("A PUG with that name already exists. Please try a different name.")
            return

        # Check if the input included a PUG name
        if not pug_name:
            await message.channel.send("I couldn't find a PUG name. Please try again.")
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
            await message.channel.send(f"You're already in the PUG `{existing_pug.name}`.")
            return

        # Attempt to add the user to the PUG
        for pug in pugs:
            if pug.name == pug_name:
                if pug.add_player(message.author):
                    await update_status(message.channel, pug)
                else:
                    await message.channel.send(f"The PUG `{pug_name}` is full.")

                return

        await message.channel.send(f"The PUG `{pug_name}` doesn't exist.")



    ########################################
    #### Leaving a pug
    ########################################
    if user_input["command"] == "leave":
        # Check if a user is in a PUG
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if existing_pug:
            existing_pug.remove_player(message.author)
            await update_status(message.chanel, existing_pug)
            return

        await message.channel.send("You're not currently in any PUG.")


    ########################################
    #### Deleting a pug
    ########################################
    if user_input["command"] == "cancel":
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if owned_pug:
            await message.channel.send(f"Successfully deleted the PUG `{owned_pug.name}`.")
            await owned_pug.status.delete()

            # Remove all references to the PUG
            pugs.remove(owned_pug)
            # del owned_pug
        else:
            await message.channel.send("You don't have any PUGs.")


    #########################################
    #### Starting a pug
    ########################################
    if user_input["command"] == "start":
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if owned_pug:
            # If every team has chosen a channel
            if all(team.channel for team in owned_pug.teams):
                # Move the team members to their channel
                for team in owned_pug.teams:
                    for member in team.members:
                        await member.move_to(team.channel)

                await message.channel.send(f"Successfully started the PUG `{owned_pug.name}`.")
                owned_pug.active = 1

                await update_status(message.channel, owned_pug)

            else:
                await message.channel.send("Not all teams have chosen their channel yet.")
        else:
            await message.channel.send("You don't have any PUGs.")


    ########################################
    #### Finishing a pug
    ########################################
    if user_input["command"] == "finish":
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if owned_pug:
            await message.channel.send(f"Successfully stopped the PUG `{owned_pug.name}`.")
            owned_pug.active = 2

            await update_status(message.channel, owned_pug)

            # Delete all references to the PUG -- it's done
            pugs.remove(owned_pug)
            # del owned_pug
        else:
            await message.channel.send("You don't have any PUGs.")


    ########################################
    #### Randomize teams
    ########################################
    if user_input["command"] == "random":
        owned_pug = find_in_list(lambda pug: pug.creator == message.author, pugs)
        if owned_pug:
            arguments = user_input["arguments"]
            try:
                num_teams = int(arguments[-1])
            except:
                await message.channel.send("That wasn't a valid number. Please try again.")
                return

            if num_teams > len(owned_pug.players):
                await message.channel.send("There aren't enough people for that many teams. Please try again.")
                return

            if num_teams <= 0:
                await message.channel.send("The number of teams must be positive. Please try again.")
                return

            # Clear teams
            owned_pug.teams = []

            if len(arguments) == 1:
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
            elif len(arguments) == 2 and arguments[0] == "captains":
                # Randomly pick captains
                players_copy = owned_pug.players.copy()
                shuffle(players_copy)
                for i in range(num_teams):
                    owned_pug.add_team(players_copy[i])

            await update_status(message.channel, owned_pug)
        else:
            await message.channel.send("You don't have any PUGs.")
    

    ########################################
    #### Creating a team
    ########################################
    if user_input["command"] == "team":
        if len(message.content) > 50:
            await message.channel.send("The input is too long. Try something shorter.")
            return

        team_name = user_input["arguments"]
        
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if not existing_pug:
            await message.channel.send("You're not in any active PUGs.")
            return
        if team_name in map(lambda team: team.name, existing_pug.teams):
            await message.channel.send("A team with that name already exists.")
            return
        if existing_pug.find_team(message.author):
            await message.channel.send("You're already in a team.")
            return

        existing_pug.add_team(message.author, team_name)
        # await message.channel.send(f"Successfully created the team `{team_name}`.")
        await update_status(message.channel, existing_pug)


    ########################################
    #### Renaming a team
    ########################################
    if user_input["command"] == "rename":
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if existing_pug:
            if existing_pug.is_captain(message.author):
                # If the user is a captain
                new_name = user_input["arguments"]

                # Check if the name is used somewhere else in the pug
                if not all(not team.name == new_name for team in existing_pug.teams):
                    await message.channel.send("A team with that name already exists.")
                    return

                # If everything goes well
                existing_pug.find_team(message.author).name = new_name
                
                await update_status(message.channel, existing_pug)
            else:
                # If the user is not a captain
                await message.channel.send("Only captains can change a team name.")
        else:
            await message.channel.send("You're not currently in a PUG.")


    ########################################
    #### Picking a team member
    ########################################
    if user_input["command"] == "pick":
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if existing_pug:
            if existing_pug.is_captain(message.author):
                # If the user is a captain
                try:
                    player_num = int(user_input["arguments"])
                except:
                    await message.channel.send("That wasn't a valid number. Try again.")
                    return

                # If the number is not in the correct range or if the chosen player is on a team already
                if not 1 <= player_num <= len(existing_pug.players) or existing_pug.find_team(existing_pug.players[player_num-1]):
                    await message.channel.send("That wasn't a valid pick. Try again.")
                    return

                # If everything goes well
                existing_pug.add_to_team(message.author, player_num)
                await message.channel.send(f"Added {existing_pug.players[player_num-1]} to your team.")
                
                await update_status(message.channel, existing_pug)
            else:
                # If the user is not a captain
                await message.channel.send("Only captains can pick players.")
        else:
            await message.channel.send("You're not currently in a PUG.")


    ########################################
    #### Kicking a team member
    ########################################
    if user_input["command"] == "kick":
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if existing_pug:
            if existing_pug.is_captain(message.author):
                # If the user is a captain
                try:
                    player_num = int(user_input["arguments"])
                except:
                    await message.channel.send("That wasn't a valid number. Try again.")
                    return

                # If everything goes well
                current_team = existing_pug.find_team(message.author)
                if not 1 <= player_num <= len(current_team.members):
                    await message.channel.send("That wasn't a valid number. Try again.")
                    return

                # await message.channel.send(f"Removed {current_team.members[player_num-1]} from your team.")
                existing_pug.remove_from_team(message.author, player_num)
                
                await update_status(message.channel, existing_pug)
            else:
                # If the user is not a captain
                await message.channel.send("Only captains can pick players.")
        else:
            await message.channel.send("You're not currently in a PUG.")


    ########################################
    #### Pick a channel
    ########################################
    if user_input["command"] == "channel":
        existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
        if existing_pug:
            if existing_pug.is_captain(message.author):
                # If the user is a captain
                # Find all voice channels and ist them
                channels = [channel for channel in message.guild.voice_channels]

                channel_message = "Pick a channel:\n"
                for (i, channel) in enumerate(channels):
                    channel_message += f"{i+1}. {channel}\n"
                await message.channel.send(channel_message)

                # Wait for input
                result = await client.wait_for("message", check=lambda m: m.author == message.author)
                try:
                    index = int(result.content)-1
                except:
                    await message.channel.send("That wasn't a valid number. Try again.")
                    return
                
                # Check if the channel has been taken
                if all(not team.channel == channels[index] for team in existing_pug.teams):
                    existing_pug.find_team(message.author).channel = channels[index]
                    await message.channel.send(f"You have successfully set your team's channel to {channels[index].name}.")
                    
                    await update_status(message.channel, existing_pug)
                else:
                    await message.channel.send("That channel has been taken already. Try again.")
            else:
                # If the user is not a captain
                await message.channel.send("Only captains can pick a channel.")
        else:
            await message.channel.send("You're not currently in a PUG.")

client.run(TOKEN)