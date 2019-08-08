# Written by greenlittleapple (Marcus Wong)

import discord
from discord.ext import commands
import head
import command_handler
import botutils
import reddit_handler

if __name__ == '__main__':
    @head.client.event
    async def on_ready():
        botutils.write_to_log('Logged in to Discord')
        print('Logged in as')
        print(head.client.user.name)
        print(head.client.user.id)
        print('------')
        await command_handler.add_emojis_to_msgs()
        # reddit_handler.start_retrieve_UCI(True)


    @head.client.event
    async def on_message(message: discord.Message):
        await command_handler.handle_message(message)


    @head.client.event
    async def on_raw_reaction_add(r: discord.RawReactionActionEvent):
        await command_handler.handle_emote_add(r)


    @head.client.event
    async def on_raw_reaction_remove(r: discord.RawReactionActionEvent):
        await command_handler.handle_emote_remove(r)


    head.client.run(head.token)
    # head.client.run(head.self_token, bot=False)
