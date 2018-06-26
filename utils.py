import discord
from config import prefix

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
        "command": split_string[0],
        "arguments": " ".join(split_string[1:])
    }

def find_in_list(query, _list):
    """
    From a list, returns the first element that satisfies the query
    """
    item = list(filter(query, _list))
    return item[0] if item else None

async def update_status(channel, pug):
    """
    Replace the old pug embed with an updated one in the given channel
    """
    if pug.active == 0:   # PUG hasn't started
        color = discord.Color.red()
        footer_text = "This PUG has not started yet."
    elif pug.active == 1: # PUG has started
        color = discord.Color.green()
        footer_text = "This PUG has started."
    elif pug.active == 2: # PUG finished
        color = discord.Color.blue()
        footer_text = "This PUG has ended."

    new_status = discord.Embed(
        title=pug.name,
        type="rich",
        color=color
    )

    new_status.set_footer(text=footer_text)

    new_status.set_author(
        name=pug.creator.name,
        icon_url=pug.creator.avatar_url
    )

    new_status.add_field(
        name="Player Count",
        value=f"Current number of players: {len(pug.players)}/{pug.max_size}",
        inline=False
    )

    if pug.teams:
        for team in pug.teams:
            if team.members:
                member_list = ""
                for (i, player) in enumerate(team.members):
                    member_list += f"{i+1}. {player.name}\n"

                channel_message = f" (Channel: {team.channel})" if team.channel else ""
                new_status.add_field(
                    name=f"Team {team.name} — Captain: {team.members[0]}{channel_message}",
                    value=member_list,
                    inline=True
                )

    if pug.players:
        player_list = ""
        for (i, player) in pug.remaining_players():
            if i > 0:
                player_list += f"{i}. {player.name}\n"
            else:
                player_list += f"~~{i}. {player.name}~~\n"

        new_status.add_field(
            name="Player List",
            value=player_list,
            inline=False
        )

    if pug.status:
        await pug.status.delete()
    pug.status = await channel.send(embed=new_status)