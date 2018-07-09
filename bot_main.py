# Written by greenlittleapple (Marcus Wong)

import discord
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
        reddit_handler.start_retrieve_UCI(True)

    @head.client.event
    async def on_message(message: discord.Message):
        await command_handler.handle_message(message)

    head.client.run(head.token)
