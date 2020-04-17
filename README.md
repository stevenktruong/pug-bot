# `pug-bot`

A bot for managing pick-up games (aka scrims) on Discord.

The bot is programmed entirely in Python 3, and it makes use of the [discord.py](https://github.com/Rapptz/discord.py) package.

This bot _probably_ shouldn't be used to learn from. I didn't use the `commands` extension from `discord.ext` since this bot was a learning project for me--this is my first Python project and I didn't want to program with too much abstraction.

## Introduction

The creation of this bot was inspired by the daily League of Legends 10-mans in my guild.

The bot helps you keep track of teams and players, and it can also randomize teams for you. Another nice feature is that each team can pick a voice channel, and the bot will automatically move teams to their picked channels. After completing a round of games (i.e., when you run `..stop`), the lobby owner has the option to move all players to one voice channel automatically.

![example of usage](https://imgur.com/qv5WTkJ.png)

## Dependencies

[`discord.py`](https://github.com/Rapptz/discord.py)

If `pip` is installed, you can install the package with `make`.

## Usage

The bot searches for the environment variable `TOKEN` with your API token. If you don't know how to set an environment variable, then you can just place it in `pug-bot/apitoken.py`. To start the bot, just run `make start`.

The main flow for this bot is as follows:

1. Create a PUG
2. Have players join the PUG
3. Pick teams and channels
4. Start the PUG
5. Stop the PUG
6. Repeat or close it

Here's the list of commands:

| Command                     | Action                                                                                                     |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------- |
| `..help`                    | `pug-bot` will private message you a list of commands and their usage (i.e., basically everything in here) |
| `..create [name] [size]`    | Create a PUG with the given name and size                                                                  |
| `..owner [number]`          | Change the PUG owner                                                                                       |
| `..join [name]`             | Join the PUG with the given name                                                                           |
| `..leave`                   | Leave the PUG you're currently in                                                                          |
| `..cancel`                  | Delete the PUG you created                                                                                 |
| `..start`                   | Starts your PUG and moves teams to their channels                                                          |
| `..stop`                    | Stops the PUG and move players to a channel                                                                |
| `..close`                   | Close a PUG, i.e., you can't interact with the PUG anymore                                                 |
| `..reset`                   | Remove all teams in your PUG                                                                               |
| `..refresh`                 | Refresh the message with the PUG status                                                                    |
| `..remove [numbers]`        | Remove players from your PUG                                                                               |
| `..random [teams]`          | Randomly create teams in your PUG, if there're enough people                                               |
| `..random captains [teams]` | Randomly assign captains in your PUG, if there're enough people                                            |
| `..team [team name]`        | Create a team with the listed name and captain it                                                          |
| `..captain [number]`        | Make one of your teammates a captain                                                                       |
| `..rename [team name]`      | Rename the team you're the captain of                                                                      |
| `..pick [numbers]`          | Pick teammates from the player list                                                                        |
| `..kick [numbers]`          | Kick teammates from your team                                                                              |
| `..channel`                 | Select your team's voice channel                                                                           |
| `..addwin [number]`         | Add a win to a team                                                                                        |
| `..removewin [number]`      | Remove a win from a team                                                                                   |
| `..roll [number] [number]`  | Randomly pick a number                                                                                     |

​
