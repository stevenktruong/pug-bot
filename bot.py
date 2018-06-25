import discord
import re
import os
from pug import Pug
from utils import *
import config

TOKEN = os.getenv('TOKEN') if os.getenv('TOKEN') else config.TOKEN

client = discord.Client()

# server_list is of the form
# {
#     server: set()
# }
server_list = {}

prefix = ".."

@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    ########################################
    #### Help function
    ########################################
    if message.content == f"{prefix}help":
        help_message = "```"
        help_message += f"{prefix}create [pug name] [size] - Create a PUG with the given name and size.\n"
        help_message += f"{prefix}join [pug name] - Join a PUG with the given name.\n"
        help_message += f"{prefix}leave - Leave whatever PUG you're in.\n"
        help_message += f"{prefix}cancel - If you've created a PUG, this deletes it.\n"
        help_message += f"{prefix}start - If you've created a PUG, this starts it. This moves all players to the chosen channels and closes the create lobby.\n"
        help_message += f"{prefix}team [team name] - Once you're in a PUG, you can create your own team with the given name.\n"
        help_message += f"{prefix}pick [number] - If you're team captain, you can pick your teammates with this.\n"
        help_message += f"{prefix}kick [number] - If you're team captain, you can kick your teammates with this.\n"
        help_message += f"{prefix}channel - If you're team captain, you can select a voice channel for your team. Enter the number of the voice channel you want.\n"
        help_message += "```"
        await client.send_message(message.author, help_message)

    # Add the server to the servers list if it's not in it already
    if not message.server.name in server_list.keys():
        server_list[message.server.name] = set()

    pugs = server_list[message.server.name]

    ########################################
    #### Creating a pug
    ########################################
    if message.content.startswith(f"{prefix}create "):
        # Check if input is too long
        if len(message.content) > 100:
            await client.send_message(message.channel, "The input is too long. Try something shorter.")
            return

        # Check if a user already has a PUG or not
        owned_pug = list(filter(lambda pug: pug.creator == message.author, pugs))
        if owned_pug:
            await client.send_message(message.channel, f"You already have an active PUG named `{owned_pug[0].name}`.")
            return

        trimmed_message = message.content.split(f"{prefix}create ").pop()
        size_string = trimmed_message.split().pop()

        # Scrape the desired PUG size
        try:
            pug_size = int(size_string)
        except:
            await client.send_message(message.channel, "I couldn't find a team size.")
            return

        if not 0 < pug_size <= 100:
            await client.send_message(message.channel, "A team size must lie between 1 and 100. Please try again.")
            return

        pug_name = trimmed_message[0:-(len(size_string)+1)]

        # Check if a PUG with the desired name exists
        existing_pug = list(filter(lambda pug: pug.name == pug_name, pugs))
        if existing_pug:
            await client.send_message(message.channel, "A PUG with that name already exists. Please try a different name.")
            return

        # Check if the input included a PUG name
        if not pug_name:
            await client.send_message(message.channel, "I couldn't find a PUG name. Please try again.")
            return

        # Create the pug
        new_pug = Pug(name=pug_name, creator=message.author, max_size=pug_size, teams=[], players=[], active=None)
        pugs.add(new_pug)
        # await client.send_message(message.author, f"Created the PUG `{pug_name}`.")

        # Send the pug status embed
        new_pug.status = await client.send_message(message.channel, embed=pug_status(new_pug))


    ########################################
    #### Joining a pug
    ########################################
    if message.content.startswith(f"{prefix}join "):
        pug_name = message.content.split(f"{prefix}join ").pop()
        
        # Check if a user is already in a PUG
        existing_pug = list(filter(lambda pug: message.author in pug.players, pugs))
        if existing_pug:
            await client.send_message(message.channel, f"You're already in the PUG `{existing_pug[0].name}`.")
            return

        # Attempt to add the user to the PUG
        for pug in pugs:
            if pug.name == pug_name:
                if pug.add_player(message.author):
                    await client.delete_message(pug.status)
                    pug.status = await client.send_message(message.channel, embed=pug_status(pug))
                    
                else:
                    await client.send_message(message.channel, f"The PUG `{pug_name}` is full.")

                return

        await client.send_message(message.channel, f"The PUG `{pug_name}` doesn't exist.")



    ########################################
    #### Leaving a pug
    ########################################
    if message.content.startswith(f"{prefix}leave"):
        # Check if a user is in a PUG
        existing_pug = list(filter(lambda pug: message.author in pug.players, pugs))
        if existing_pug:
            existing_pug[0].remove_player(message.author)
            await client.delete_message(existing_pug[0].status)
            # await client.send_message(message.author, f"You have left the PUG `{existing_pug[0].name}`.")
            existing_pug[0].status = await client.send_message(message.channel, embed=pug_status(existing_pug[0]))
            return

        await client.send_message(message.channel, "You're not currently in any PUG.")


    ########################################
    #### Deleting a pug
    ########################################
    if message.content == f"{prefix}cancel":
        owned_pug = list(filter(lambda pug: pug.creator == message.author, pugs))
        if owned_pug:
            await client.send_message(message.channel, f"Successfully deleted the PUG `{owned_pug[0].name}`.")
            await client.delete_message(owned_pug[0].status)
            pugs.remove(owned_pug[0])
            del owned_pug[0]
        else:
            await client.send_message(message.channel, "You don't have any PUGs.")

    ########################################
    #### Starting a pug
    ########################################
    if message.content == f"{prefix}start":
        owned_pug = list(filter(lambda pug: pug.creator == message.author, pugs))
        if owned_pug:
            # If every team has chosen a channel
            if all(team.channel for team in owned_pug[0].teams):
                # Move the team members to their channel
                for team in owned_pug[0].teams:
                    for member in team.members:
                        await client.move_member(member, team.channel)

                await client.send_message(message.channel, f"Successfully started the PUG `{owned_pug[0].name}`.")
                owned_pug[0].active = True
                await client.delete_message(owned_pug[0].status)
                owned_pug[0].status = await client.send_message(message.channel, embed=pug_status(owned_pug[0]))

                # Delete all references to the PUG -- it's done
                pugs.remove(owned_pug)
                del owned_pug[0]
            else:
                await client.send_message(message.channel, "Not all teams have chosen their channel yet.")
        else:
            await client.send_message(message.channel, "You don't have any PUGs.")

    # ########################################
    # #### Stopping a pug
    # ########################################
    # if message.content == f"{prefix}stop":
    #     owned_pug = list(filter(lambda pug: pug.creator == message.author, pugs))
    #     if owned_pug:
    #         await client.send_message(message.channel, f"Successfully stopped the PUG `{owned_pug[0].name}`.")
    #         owned_pug[0].active = False
    #         await client.delete_message(owned_pug[0].status)
    #         owned_pug[0].status = await client.send_message(message.channel, embed=pug_status(owned_pug[0]))
    #     else:
    #         await client.send_message(message.channel, "You don't have any PUGs.")
    
    ########################################
    #### Creating a team
    ########################################
    if message.content.startswith(f"{prefix}team "):
        if len(message.content) > 50:
            await client.send_message(message.channel, "The input is too long. Try something shorter.")
            return

        team_name = message.content.split(f"{prefix}team ").pop()
        
        existing_pug = list(filter(lambda pug: message.author in pug.players, pugs))
        if not existing_pug:
            await client.send_message(message.channel, "You're not in any active PUGs.")
            return
        if team_name in map(lambda team: team.name, existing_pug[0].teams):
            await client.send_message(message.channel, "A team with that name already exists.")
            return
        if existing_pug[0].find_team(message.author):
            await client.send_message(message.channel, "You're already in a team.")
            return

        existing_pug[0].add_team(message.author, team_name)
        # await client.send_message(message.channel, f"Successfully created the team `{team_name}`.")
        await client.delete_message(existing_pug[0].status)
        existing_pug[0].status = await client.send_message(message.channel, embed=pug_status(existing_pug[0]))


    ########################################
    #### Picking a team member
    ########################################
    if message.content.startswith(f"{prefix}pick "):
        existing_pug = list(filter(lambda pug: message.author in pug.players, pugs))
        if existing_pug:
            if existing_pug[0].is_captain(message.author):
                # If the user is a captain
                try:
                    player_num = int(message.content.split(f"{prefix}pick ").pop())
                except:
                    await client.send_message(message.channel, "That wasn't a valid number. Try again.")
                    return

                # If the number is not in the correct range or if the chosen player is on a team already
                if not 1 <= player_num <= len(existing_pug[0].players) or existing_pug[0].find_team(existing_pug[0].players[player_num-1]):
                    await client.send_message(message.channel, "That wasn't a valid pick. Try again.")
                    return

                # If everything goes well
                existing_pug[0].add_to_team(message.author, player_num)
                await client.send_message(message.channel, f"Added {existing_pug[0].players[player_num-1]} to your team.")
                await client.delete_message(existing_pug[0].status)
                existing_pug[0].status = await client.send_message(message.channel, embed=pug_status(existing_pug[0]))
            else:
                # If the user is not a captain
                await client.send_message(message.channel, "Only captains can pick players.")
        else:
            await client.send_message(message.channel, "You're not currently in a PUG.")


    ########################################
    #### Kicking a team member
    ########################################
    if message.content.startswith(f"{prefix}kick "):
        existing_pug = list(filter(lambda pug: message.author in pug.players, pugs))
        if existing_pug:
            if existing_pug[0].is_captain(message.author):
                # If the user is a captain
                try:
                    player_num = int(message.content.split(f"{prefix}kick ").pop())
                except:
                    await client.send_message(message.channel, "That wasn't a valid number. Try again.")
                    return

                # If everything goes well
                current_team = existing_pug[0].find_team(message.author)
                if not 1 <= player_num <= len(current_team.members):
                    await client.send_message(message.channel, "That wasn't a valid number. Try again.")
                    return

                existing_pug[0].remove_from_team(message.author, player_num)
                await client.send_message(message.channel, f"Removed {existing_pug[0].players[player_num-1]} from your team.")
                await client.delete_message(existing_pug[0].status)
                existing_pug[0].status = await client.send_message(message.channel, embed=pug_status(existing_pug[0]))
            else:
                # If the user is not a captain
                await client.send_message(message.channel, "Only captains can pick players.")
        else:
            await client.send_message(message.channel, "You're not currently in a PUG.")

    ########################################
    #### Pick a channel
    ########################################
    if message.content.startswith(f"{prefix}channel"):
        existing_pug = list(filter(lambda pug: message.author in pug.players, pugs))
        if existing_pug:
            if existing_pug[0].is_captain(message.author):
                # If the user is a captain
                # Find all voice channels and ist them
                channels = []
                for channel in message.server.channels:
                    if channel.type == discord.ChannelType.voice:
                        channels.append(channel)

                channel_message = "Pick a channel:\n"
                for (i, channel) in enumerate(channels):
                    channel_message += f"{i+1}. {channel}\n"
                await client.send_message(message.channel, channel_message)

                # Wait for input
                result = await client.wait_for_message(author=message.author)
                try:
                    index = int(result.content)-1
                except:
                    await client.send_message(message.channel, "That wasn't a valid number. Try again.")
                    return
                
                # Check if the channel has been taken
                if all(not team.channel == channels[index] for team in existing_pug[0].teams):
                    existing_pug[0].find_team(message.author).channel = channels[index]
                    await client.send_message(message.channel, f"You have successfully set your team's channel to {channels[index].name}.")
                    await client.delete_message(existing_pug[0].status)
                    existing_pug[0].status = await client.send_message(message.channel, embed=pug_status(existing_pug[0]))
                else:
                    await client.send_message(message.channel, "That channel has been taken already. Try again.")
            else:
                # If the user is not a captain
                await client.send_message(message.channel, "Only captains can pick a channel.")
        else:
            await client.send_message(message.channel, "You're not currently in a PUG.")

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

client.run(TOKEN)