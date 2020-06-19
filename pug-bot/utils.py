import discord
import time
from .config import *

def parse_command(string):
    """
    Commands with arguments are guaranteed to start with '[prefix][command] '
    For example, this function maps '..create pug name 10' to
    {
        'command': 'create',
        'arguments': 'name 10'
    }
    """
    # Remove the prefix and split the command
    split_string = string[len(prefix):].split()
    return {
        "command": split_string[0] if len(split_string) > 0 else "",
        "arguments": " ".join(split_string[1:])
    }

def find_in_list(query, _list):
    """
    From a list, returns the first element that satisfies the query
    """
    item = list(filter(query, _list))
    return item[0] if item else None

async def update_status(channel, pug, active_status=None):
    """
    Replace the old pug embed with an updated one in the given channel and update pug.active
    """
    if active_status is not None:
        pug.active = active_status
    color = PUG_EMBED_COLORS[pug.active]
    footer_text = PUG_EMBED_FOOTER_MESSAGES[pug.active]

    new_status = discord.Embed(
        title=pug.name,
        description=f"Type `{prefix}join {pug.name}` to join this lobby.\n\u200b",
        type="rich",
        color=color
    )

    new_status.set_footer(text=footer_text)

    new_status.set_author(
        name=pug.owner.name,
        icon_url=pug.owner.avatar_url
    )

    # Player count
    new_status.add_field(
        name="Player Count",
        value=f"Current number of players: {len(pug.players)}/{pug.max_size}\n\u200b",
        inline=False
    )

    # PUG teams
    if pug.teams:
        for team in pug.teams:
            if team.members:
                member_list = f"Wins: {team.wins}\n"
                member_list += "Channel: " + (f"{team.channel}" if team.channel else "Not chosen") + "\n"
                member_list += f"`[1]` {team.members[0].name} **(Captain)**\n"
                for (i, player) in enumerate(team.members[1:]):
                    member_list += f"`[{i+2}]` {player.name}\n"
                member_list += "\u200b"

                new_status.add_field(
                    name=f"Team {team.name}",
                    value=member_list,
                    inline=False
                )

    # PUG players
    if pug.players:
        player_list = ""
        for (i, player) in pug.remaining_players():
            if i > 0:
                player_list += f"`[{i}]` {player.name}\n"
            else:
                player_list += f"`[{-i}]` ~~{player.name}~~\n"
        player_list += "\u200b"

        new_status.add_field(
            name="Player List",
            value=player_list,
            inline=True
        )

    # PUG channels
    channels = [channel for channel in channel.guild.voice_channels]

    channel_list = ""
    for (i, _channel) in enumerate(channels):
        if _channel in [team.channel for team in pug.teams]:
            channel_list += f"`[{i+1}]` ~~{_channel}~~\n"
        else:
            channel_list += f"`[{i+1}]` {_channel}\n"

    new_status.add_field(
        name="Channel List",
        value=channel_list,
        inline=True
    )

    if pug.status:
        await pug.status.delete()
    pug.status = await channel.send(embed=new_status)
    pug.channel = pug.status.channel
    pug.last_action = time.time()