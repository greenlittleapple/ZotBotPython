# Written by greenlittleapple (Marcus Wong)

import discord
import head
import command_handler

if __name__ == '__main__':

    @head.client.event
    async def on_ready():
        print('Logged in as')
        print(head.client.user.name)
        print(head.client.user.id)
        print('------')

    @head.client.event
    async def on_message(message: discord.Message):
        await command_handler.handle_message(message)

    head.client.run(head.token)
