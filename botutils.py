import discord
import head
import atexit

logfile = open('zotbot_log.txt', 'a+')
atexit.register(logfile.close)


def is_mod(user: discord.Member) -> bool:
    return user.server_permissions.administrator


# noinspection PyPep8Naming
def get_UCI() -> discord.Server:
    return head.client.get_server('341464294132678668')


def get_role_by_id(id: str, server: discord.Server) -> discord.Role:
    return discord.utils.get(server.roles, id=id)


def get_chan_by_id(id: str) -> discord.Channel:
    return head.client.get_channel(id=id)


def find_user(term: str, server: discord.Server) -> discord.User or None:
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


def check_match(server: discord.Server,
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
