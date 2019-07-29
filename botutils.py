import discord
import head
import datetime

logfile = open('zotbot_log.txt', 'a+')


def time_now() -> str:
    return str(datetime.datetime.now())


def write_to_log(data: str):
    logfile.write(time_now() + ' - ' + data + '\n')
    logfile.flush()


def is_mod(user: discord.Member) -> bool:
    return user.server_permissions.administrator


# noinspection PyPep8Naming
def get_UCI() -> discord.Guild:
    return head.client.get_guild(341464294132678668)


def get_emoji_by_id(id: int) -> discord.Emoji:
    return head.client.get_emoji(id)

def get_server_by_id(id: int) -> discord.Guild:
    return head.client.get_guild(id)


def get_role_by_id(id: int, server: discord.Guild) -> discord.Role:
    return server.get_role(id)


def get_textchan_by_id(id: int) -> discord.TextChannel:
    return head.client.get_channel(id)


async def get_fguci_msg() -> discord.Message:
    return await get_textchan_by_id(604095840025575435).fetch_message(604100765883039784)


async def get_vruci_msg() -> discord.Message:
    return await get_textchan_by_id(444291846555041797).fetch_message(445660909696974859)


def find_user(term: str, server: discord.Guild) -> discord.User or None:
    users = get_UCI().members
    for i in range(7):
        for x in users:
            matched = [
                check_match(server, term, x, True, True, False, False, False, False),
                check_match(server, term, x, True, False, False, False, False, False),
                check_match(server, term, x, False, True, False, False, False, False),
                check_match(server, term, x, False, False, True, False, False, False),
                check_match(server, term, x, False, False, False, True, False, False),
                check_match(server, term, x, False, False, False, False, True, False),
                check_match(server, term, x, False, False, False, False, False, True)
            ][i]
            if matched:
                return x
    return None


def check_match(server: discord.Guild,
                search: str,
                user: discord.User,
                username_match: bool, nickname_match: bool,
                username_start: bool, nickname_start: bool,
                username_contains: bool, nickname_contains: bool) -> bool:
    user_name = user.name.lower()
    disp_name = user.display_name.lower()
    search = search.lower()
    if username_match:
        if nickname_match:
            return check_match(server, search, user, True, False, False, False, False, False) \
                   and check_match(server, search, user, False, True, True, True, True, True)
        else:
            return search == user_name
    elif nickname_match:
        return search == disp_name
    elif username_start:
        return user_name.startswith(search)
    elif nickname_start:
        return disp_name.startswith(search)
    elif username_contains:
        return search in user_name
    elif nickname_contains:
        return search in disp_name
    return False
