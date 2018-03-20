import asyncio

import head
import botutils
import discord
import praw
from time import *

client = praw.Reddit(client_id=head.reddit_client_id,
                     client_secret=head.reddit_secret,
                     username=head.reddit_user,
                     password=head.reddit_pw,
                     user_agent='ZotBot by greenlittleapple')

botutils.write_to_log('Reddit logged on: ' + str(client.user.me()))

uci_sub = client.subreddit('UCI')
meme_subs = client.subreddit('ProgrammerHumor+dankmemes+wholesomememes')
uci_enabled = True
uci_running = False


async def retrieve_and_post_UCI():
    await head.client.wait_until_ready()
    while not head.client.is_closed and uci_enabled:
        global uci_running
        uci_running = True
        botutils.write_to_log('Checking for new posts...')
        processed = 0
        for submission in sorted(uci_sub.new(limit=5), key=lambda x: x.created_utc):
            processed += 1
            if processed == 50:  # Stop giant for loop, for some reason it gets stuck?
                break
            file = open('uci_posts.txt', 'r+')
            if not str(submission.id + "\n") in file.readlines():
                embed = discord.Embed(
                    title=submission.title[:130] + ('...' if submission.title[:130] != submission.title else ''),
                    color=discord.Color.blue(),
                    description='/u/' + str(submission.author) + ' - *' + ctime(
                        submission.created_utc - 3 * 3600) + '*\n' + submission.shortlink)
                if submission.url.endswith(tuple(['jpg', 'gif', 'png', 'jpeg', 'tiff', 'bmp', 'mp4'])):
                    # print('Set Image: ' + submission.url)
                    embed = embed.set_image(url=submission.url)
                else:
                    if hasattr(submission, 'preview'):
                        # print('Set Thumb: ' + submission.preview['images'][0]['resolutions'][0]['url'])
                        embed.set_thumbnail(url=submission.preview['images'][0]['resolutions'][0]['url'])
                    embed.add_field(name="Preview", value=(" ".join(
                        submission.selftext.split(" ")[
                        :20]) + "...\n") if submission.selftext != '' else submission.url)
                categories = set()

                def check_keyword(keyword: str) -> bool:
                    if keyword.lower() in submission.title.lower().split(
                            " ") or keyword.lower() in submission.selftext.lower().split(" "):
                        categories.add(keyword)
                        return True
                    return False

                for item in ['ICS', 'Thornton', 'Pattis', 'Klefstad', 'Gassko', '3A', '31', '32A', '33', '45C', '46']:
                    check_keyword(item)
                for item in ['Physics', '7C', '7D', '7E', 'Wu']:
                    check_keyword(item)
                for item in ['Chem', 'Bio']:
                    check_keyword(item)
                if '?' in submission.title or '?' in submission.selftext or 'question' in submission.title:
                    categories.add('Question')
                if len(categories) == 0:
                    categories.add('General')
                embed.add_field(name='Topics', value=' '.join([('**「' + x + '」**') for x in categories]), inline=False)
                try:
                    botutils.write_to_log('Trying to post...')
                    await head.client.send_message(botutils.get_chan_by_id("421828948159365120"), embed=embed)
                    botutils.write_to_log('Submission Posted: ' + submission.title)
                except Exception as e:
                    botutils.write_to_log('ERROR: ' + str(e) + '\n' + 'Error in Submission: ' + submission.title)
                finally:
                    with open('uci_posts.txt', 'a') as write_file:
                        write_file.write(submission.id + "\n")
                        write_file.flush()
        file.close()
        uci_running = False
        await asyncio.sleep(60)
    uci_running = False
    botutils.write_to_log('client closed: ' + head.client.is_closed + ', uci_enabled: ' + uci_enabled)
    if head.client.is_closed:
        head.client.run(head.token)


def start_retrieve_UCI(start: bool):
    global uci_enabled
    if start and not uci_running:
        uci_enabled = True
        head.client.loop.create_task(retrieve_and_post_UCI())
    elif not start and uci_running:
        uci_enabled = False


start_retrieve_UCI(True)
