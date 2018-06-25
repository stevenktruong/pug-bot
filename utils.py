import discord

# Show the PUG status
def pug_status(pug):
    color = discord.Color.green() if pug.active else discord.Color.red()

    pug_embed = discord.Embed(
        title=pug.name,
        type="rich",
        color=color
    )

    if pug.active:
        pug_embed.set_footer(text="This PUG has started.")
    else:
        pug_embed.set_footer(text="This PUG has not started yet.")

    pug_embed.set_author(
        name=pug.creator.name,
        icon_url=pug.creator.avatar_url
    )

    pug_embed.add_field(
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
                pug_embed.add_field(
                    name=f"Team {team.name} — Captain: {team.members[0]}{channel_message}",
                    value=member_list,
                    inline=False
                )

    if pug.players:
        player_list = ""
        for (i, player) in pug.remaining_players():
            if i > 0:
                player_list += f"{i}. {player.name}\n"
            else:
                player_list += f"~~{i}. {player.name}~~\n"

        pug_embed.add_field(
            name="Player List",
            value=player_list,
            inline=False
        )

    return pug_embed
