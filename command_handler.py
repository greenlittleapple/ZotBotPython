# Written by greenlittleapple (Marcus Wong)


import discord
import head
import botutils
import facts
import reddit_handler

noPerm = "ERROR: You do not have permission to use this command."


async def handle_message(message: discord.Message):
    client = head.client
    lower_case_message = message.content.lower()
    if not message.author.bot:
        if lower_case_message.startswith('zot zot zot'):
            await client.send_message(message.channel, content='ZOT ZOT ZOT!')
        elif lower_case_message.startswith('z!'):
            command = lower_case_message[2:].rstrip()  # type: str
            out_message = ''

            if command == 'apple':
                out_message = "Why are you typing a command that doesn't exist? Shame on you."
            elif command == 'bustazot':
                client.send_file(message.channel, "", content="MAP OF RESTROOMS AT UCI"),
            elif command == 'calendar':
                out_message = "https://www.reg.uci.edu/calendars/quarterly/2017-2018/quarterly17-18.html"
            elif command == 'clubs':
                out_message = "Sorry, I don't know what to do with this command. Please give me suggestions! (e.g. letting you search for keywords)"
            elif command == 'fact':
                out_message = facts.Facts.get_fact()
            elif command == 'food':
                out_message = "http://www.food.uci.edu/dining.php"
            elif command == 'help':
                out_message = "```Available commands are: ```" + "\n" + "`z!calendar`, `z!clubs`, `z!fact`, `z!find`, `z!food`, `z!help`, `z!housing`, `z!meme`, `z!portal`, `z!planner`, `z!playing`, `z!report`, `z!services`, `z!shuttle`, `z!zot`" + "\n\n" + "```Type \"z!help [command]\" for more info regarding a command. (e.g. \"z!help fact\")" + "\n" + "I was made by Apple 🍏#4472, please contact him if you have any suggestions or issues! v" + head.version + "```"
            elif command == 'help calendar':
                out_message = "`z!calendar: Provides a link to the UCI Academic Calendar.`"
            elif command == 'help clubs':
                out_message = "`z!clubs: Provides a link to UCI Campus Organizations.`"
            elif command == 'help food':
                out_message = "`z!food: Provides a link to UCI Dining Locations.`"
            elif command == 'help fact':
                out_message = "`z!fact: Gives a random UCI/Anteater fact!`"
            elif command == 'help find':
                out_message = "`z!find [user]: Finds a user based on a search query.`"
            elif command == 'help help':
                out_message = "`ERROR: INFINITE RECURSION DETECT3&89 913jf iaafffffff`"
            elif command == 'help housing':
                out_message = "`z!housing: Provides a link to UCI Housing.`"
            elif command == 'help meme':
                out_message = "z!meme: Gives a random UCI meme!"
            elif command == 'help planner':
                out_message = \
                    "`z!planner: Provides a link to CourseEater UCI's (unofficial course planning site.`"
            elif command == 'help playing':
                out_message = "z!playing [game]: Lists all users on the server playing that game."
            elif command == 'help portal':
                out_message = "`z!portal: Provides a link to the ZotPortal.`"
            elif command == 'help report':
                out_message = "`z!report: Reports a user to the moderation team. Use: z!report [user] [reason]`"
            elif command == 'help services':
                out_message = "`z!services: Provides a link to UCI Student Services.`"
            elif command == 'help shuttle':
                out_message = "`z!shuttle: Provides info about the Anteater Express.`"
            elif command == 'help zot':
                out_message = \
                    "Put your thumb to your middle and ring fingers, raise your index and pinky and bring your thumb back! ZOT ZOT ZOT!"
            elif command == 'housing':
                out_message = "https://www.housing.uci.edu/"
            elif command == 'meme':
                pass
            elif command == 'planner':
                out_message = "https://courseeater.com/"
            elif command == 'portal':
                out_message = "https://portal.uci.edu/"
            elif command == 'services':
                out_message = "https://www.admissions.uci.edu/discover/student-life/services.php"
            elif command == 'sushi':
                out_message = "╮(╯▽╰)╭"
            elif command == 'zot':
                out_message = "ZOT ZOT ZOT!"

            if command.startswith('playing'):
                await check_playing(message)
            elif command.startswith("warn"):
                if botutils.is_mod(message.author):
                    await warn(message)
                else:
                    out_message = noPerm
            elif command.startswith("unwarn"):
                if botutils.is_mod(message.author):
                    await unwarn(message)
                else:
                    out_message = noPerm
            elif command.startswith("report"):
                await report(message)
            elif command.startswith("find"):
                found_user = botutils.find_user(command[5:], message.server)
                if found_user is not None:
                    out_message = found_user.display_name
                else:
                    out_message = "ERROR: Could not find user."
            if out_message != '':
                await client.send_message(message.channel, content=out_message)


async def check_playing(message: discord.Message):
    client = head.client
    if message.content.lower().rstrip() == "z!playing":
        client.send_message(message.channel, content="ERROR: Please input a game name! (e.g. z!playing PUBG)")
    else:
        game = message.content.rstrip()[10:]
        if game.lower() in ["cs:go", "csgo", "counter strike global offensive"]:
            game = "Counter-Strike Global Offensive"
        if game.lower() in ["league", "lol"]:
            game = "League of Legends"
        if game.lower() in ["ow"]:
            game = "Overwatch"
        if game.lower() in ["osu"]:
            game = "osu!"
        if game.lower() in ["wow"]:
            game = "World of Warcraft"
        users = message.server.members  # type: list
        players = []
        for x in users:
            playing = x.game.name if x.game is not None else ""
            if playing.lower() == game.lower():
                players.append(x)
        player_list = "```fix\n"
        for user in players:
            player_list += user.display_name
            if user.display_name != user.name:
                player_list += " (" + user.name + "#" + user.discriminator + ")"
            player_list += "\n"
        player_list += "```"

        if len(players) == 0:
            await client.send_message(message.channel, content="Looks like no one is playing " + game + "!")
        else:
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color(25764),
                                                                           title="Current users playing " + game + " - " + str(
                                                                               len(players)), description=player_list))


async def warn(message: discord.Message, automod: bool = False):
    msg = message.content.rstrip()[7:]
    reason = "Breaking a server rule" if msg[len(msg.split(" ")[0])] == '' else msg[len(msg.split(" ")[0])]
    target = message.mentions[0] if len(message.mentions) > 0 else botutils.find_user(msg.split(" ")[0], message.server)  # type: discord.Member
    moderator = message.author  # type: discord.Member
    if target is not None:
        if botutils.get_role_by_id("350330574134706176", message.server) not in target.roles:
            await head.client.add_roles(target, botutils.get_role_by_id("350330574134706176", message.server))
            # Embed message for PMing warned user
            embed = discord.Embed(title="Warned on UCI Server", color=discord.Color.red())
            embed.add_field(name="Moderator", value=moderator.display_name + "#" + str(moderator.discriminator),
                            inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await head.client.send_message(target, embed=embed)
            await head.client.send_message(target,
                                           content="You will be banned on your second warning. If this warning was given in error, please contact the moderator.")
            # Embed WARN message for #mod-log
            embed = discord.Embed(title="Warning Given", color=discord.Color.red())
            embed.add_field(name="Moderator", value=moderator.display_name + "#" + str(moderator.discriminator),
                            inline=False)
            embed.add_field(name="User", value=target.name + "#" + str(target.discriminator), inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await head.client.send_message(botutils.get_chan_by_id("342545356531302413"), embed=embed)
            out_message = "Successfully warned " + target.display_name
        else:
            await head.client.kick(target)
            embed = discord.Embed(title="Kick Given", color=discord.Color.red())
            embed.add_field(name="Moderator", value=moderator.display_name + "#" + str(moderator.discriminator),
                            inline=False)
            embed.add_field(name="User", value=target.name + "#" + str(target.discriminator), inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await head.client.send_message(botutils.get_chan_by_id("342545356531302413"), embed=embed)
            out_message = "User " + target.display_name + " kicked."
    else:
        out_message = "ERROR: Please input a user to warn."
    await head.client.send_message(message.channel, content=out_message)

async def unwarn(message: discord.Message):
    msg = message.content[9:]
    target = message.mentions[0] if len(message.mentions) > 0 else botutils.find_user(msg, message.server)
    if target is not None:
        if botutils.get_role_by_id("350330574134706176", message.server) in target.roles:
            await head.client.remove_roles(target, botutils.get_role_by_id("350330574134706176", message.server))
            out_message = "Warning successfully removed."
        else:
            out_message = "ERROR: User does not have a warning."
    else:
        out_message = "ERROR: Please input a user to unwarn."
    await head.client.send_message(message.channel, out_message)

async def report(message: discord.Message):
    msg = message.content[9:] # type: str
    author = message.author # type: discord.Member
    user_search = msg.split(" ")[0]
    target = botutils.find_user(user_search, message.server) if user_search != '' else None # type: discord.Member
    if target is not None:
        reason = msg[len(user_search) + 1:]
        if reason == '':
            await head.client.send_message(author, content="ERROR: Please give a reason in your report! (Ex: z!report [user] [reason])")
        else:
            embed = discord.Embed(title="Report Submitted", color=discord.Color.red())
            embed.add_field(name="Reporter", value=author.name + "#" + str(author.discriminator), inline=False)
            embed.add_field(name="User", value=target.name + "#" + str(target.discriminator), inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await head.client.send_message(botutils.get_chan_by_id("342545356531302413"), content="<@&342539333015699457>")
            await head.client.send_message(botutils.get_chan_by_id("342545356531302413"), embed=embed)
            await head.client.send_message(author, content="Report successfully submitted for user " + target.display_name + "#" + target.discriminator + ", thank you for your help!")
    else:
        await head.client.send_message(author, "ERROR: Please input a person to report! (Ex: z!report [user] [reason])")
    await head.client.delete_message(message)