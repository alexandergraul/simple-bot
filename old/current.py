#!python321 01:00 current.py

import asyncio
import discord
import requests
import datetime
import id
import urllib.parse
import urllib.request
PASTEBIN_KEY = '2e15e96203dacd86c46417862c41f10f'
PASTEBIN_URL = 'http://pastebin.com/api/api_post.php'
client = discord.Client()
filepath = "C:\PlatsVsSilversChatlogs"

URL = {
    'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
    'summoner_by_name': 'v{version}/summoner/by-name/{names}',
    'get_league': 'v{version}/league/by-summoner/{id}/entry',
    'get_runes': 'v{version}/summoner/{id}/runes'
}

API_VERSIONS = {
    'summoner_by_name': '1.4',
    'get_league': '2.5',
    'get_runes': '1.4'
}


class RankGetter(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def _request(self, api_url, region, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        destination = URL['base'].format(
            proxy=region,
            region=region,
            url=api_url
            )
        response = requests.get(
            destination,
            params=args
            )
        return response.json()

    # Based on Summoner name, get their info
    def _get_summoner_by_name(self, name, region):
        api_url = URL['summoner_by_name'].format(
            version=API_VERSIONS['summoner_by_name'],
            names=name
            )
        return self._request(api_url, region)

    # Based on Summoner name, get ID
    def _get_summoner_id(self, name, region):
        self.name = name.replace(" ", "").lower()
        r = self._get_summoner_by_name(self.name, region)[self.name]
        return r['id']

    # Based on Summoner ID, get their rank
    def _get_rank(self, id, region):
        try:
            api_url = URL['get_league'].format(
             version=API_VERSIONS['get_league'],
             id=id)
            league = self._request(api_url, region.rstrip())[str(id)][0]
            tier = league['tier']
            division = league['entries'][0]['division']
            return tier.title()  # + " " + division
        except:
            return "Unranked"

    # Get information based on rune page
    def _get_runes(self, id, region):
        api_url = URL['get_runes'].format(
            version=API_VERSIONS['get_runes'],
            id=id
            )
        return self._request(api_url, region)

    # Get first rune page name
    def _get_rune_name(self, id, region):
        runes = self._get_runes(id, region)
        return runes[str(id)]['pages'][0]['name']

    # Returns account info that was saved (author'sName,summoner'sName,region)
    def _get_linked_account(self, name, author, region):
        id = self._get_summoner_id(name, region)
        accountLink = [[i for i in line.split(',')] for line in
                       open('linkedAccounts.txt', 'r')]
        for x in accountLink:
            if x[1] == str(id):
                if x[0].lower() == author.lower():
                    if x[2].rstrip() == region.lower():
                        return x

    def verify_rank(self, name, region):
        id = self._get_summoner_id(name, region)
        if self._get_rune_name(id, region) == "summonersplaza":
            return self._get_rank(id, region)
        else:
            return "Error"

ranks = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Masters",
         "Challenger"]
rg = RankGetter('070e0d5e-c950-47f5-8a6c-fb3a5861f70c')


@asyncio.coroutine
# manual role management for abbreviations
def verify(message):
    try:
        author = message.author
        content = message.content[8:].split(',')
        rank = rg.verify_rank(content[0], content[1].lower().strip(" "))
        rank2 = discord.utils.get(message.server.roles, name=rank)
        region = discord.utils.get(message.server.roles,
                                   name=content[1].upper().strip(" "))
        if rank == "Error":
            yield from client.send_message(message.channel, "To verify rank, "
                                           "please set the name of your first "
                                           "rune page to 'summonersplaza'.")
        elif rank == "Unranked":
            yield from client.send_message(message.channel, "You are currently "
                                           "not ranked in dynamic queue "
                                           "this season")
        else:
            roles = message.author.roles
            l = [discord.utils.get(message.server.roles, name='Verified'),
                 rank2, region]
            for r in roles:
                if r.name not in ranks:
                    l.append(discord.utils.get(message.server.roles,
                                               name=r.name))
            yield from client.replace_roles(message.author, *l)
            yield from client.send_message(message.channel,
                                           "You have been added to {}"
                                           .format(rank2))
    except:
        yield from client.send_message(message.channel,
                                       "Invalid format. Please type '!verify "
                                       "Summoner Name,Region ID'")


def add_support(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Support')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_support(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Support')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_adc(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='ADC')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_adc(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='ADC')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_mid(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Mid')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_mid(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Mid')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_top(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Top')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_top(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Top')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_jungle(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Jungle')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_jungle(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Jungle')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_bronze(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Bronze')
    roles = message.author.roles
    l = [role]
    for r in roles:
        if r.name != "Verified":
            l.append(discord.utils.get(message.server.roles, name=r.name))
    yield from client.replace_roles(message.author, *l)
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))


def del_bronze(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Bronze')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_silver(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Silver')
    roles = message.author.roles
    l = [role]
    for r in roles:
        if r.name != "Verified":
            l.append(discord.utils.get(message.server.roles, name=r.name))
    yield from client.replace_roles(message.author, *l)
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))


def del_silver(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Silver')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_gold(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Gold')
    roles = message.author.roles
    l = [role]
    for r in roles:
        if r.name != "Verified":
            l.append(discord.utils.get(message.server.roles, name=r.name))
    yield from client.replace_roles(message.author, *l)
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))


def del_gold(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Gold')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_platinum(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Platinum')
    roles = message.author.roles
    l = [role]
    for r in roles:
        if r.name != "Verified":
            l.append(discord.utils.get(message.server.roles, name=r.name))
    yield from client.replace_roles(message.author, *l)
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))


def del_platinum(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Platinum')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_diamond(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Diamond')
    roles = message.author.roles
    l = [role]
    for r in roles:
        if r.name != "Verified":
            l.append(discord.utils.get(message.server.roles, name=r.name))
    yield from client.replace_roles(message.author, *l)
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))

def add_diamondPlus(message):
    role = discord.utils.get(message.server.roles, name='Diamond +')
    roles = message.author.roles
    l = [role]
    for r in roles:
        if r.name != "Verified":
            l.append(discord.utils.get(message.server.roles, name=r.name))
    yield from client.replace_roles(message.author, *l)
    yield from client.send_message(message.channel, "You have been added to {}".format(role))

def del_diamond(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Diamond')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)

def del_diamondPlus(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Diamond +')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)

def del_masters(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Masters')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def del_challenger(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Challenger')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_na(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='NA')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_na(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='NA')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_euw(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='EUW')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_euw(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='EUW')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_oce(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='OCE')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_oce(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='OCE')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_eune(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='EUNE')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_eune(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='EUNE')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_lan(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='LAN')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_lan(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='LAN')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_brazil(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='BR')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_brazil(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='BR')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_china(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='CHINA')
    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))
    yield from client.add_roles(author, role)


def del_china(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='CHINA')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_coach(message):
    author = message.author
    required_roles = ['Diamond', 'Platinum', 'Masters', 'Challenger']
    role = discord.utils.get(message.server.roles, name='Coach')
    x = 0
    for r in author.roles:
        if r.name in required_roles:
                    x = 1
    if x == 1:
        for r in author.roles:
            if r.name == 'Verified':
                x = 2
    if x == 2:
        yield from client.send_message(message.channel,
                                       "You have been added to {}".format(role))
        yield from client.add_roles(author, role)
    elif x == 1:
        yield from client.send_message(message.channel,
                                       "You need to be verified!")
    else:
        yield from client.send_message(message.channel,
                                       "You need to be at least Platinum "
                                       "to become a coach.")


def del_coach(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Coach')
    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)

@asyncio.coroutine
def savelogs(message):
    logs = []
    command, channel, numberString = message.content.split(' ')
    chatlog = discord.utils.get(message.server.channels, name='chatlog')
    s = ""
    channel = channel.lower()
    try:
        number = int(numberString)
        for log in client.logs_from(chatlog, limit=number):
            if ("**" + channel + "**") in log.content:
                logs.append(log)
        for l in reversed(logs):
            s += l.content + "\n"
        return s
    except:
        return s

@asyncio.coroutine
def savelogs2(message):
    logs = []
    command, channel, numberString = message.content.split(' ')
    chatlog = discord.utils.get(message.server.channels, name='chatlog')
    s = ""
    channel = channel.lower()
    try:
        number = int(numberString)
        for log in client.logs_from(chatlog, limit=number):
            if ("**" + channel + "**") in log.content:
                logs.append(log)
        return reversed(logs)
    except:
        return logs


@asyncio.coroutine
def pastebin(title, content):  # used for posting a new paste
    pastebin_vars = dict(
        api_option='paste',
        api_dev_key=PASTEBIN_KEY,
        api_paste_name=title,
        api_paste_code=content,
    )
    return urllib.request.urlopen(PASTEBIN_URL,
                                        urllib.parse.urlencode(pastebin_vars)
                                        .encode('utf8')).read()


@client.event
@asyncio.coroutine
def on_member_update(before, after):  # Changes in
    nb = before.display_name
    na = after.display_name
    chatlog = discord.utils.get(before.server.channels, name='chatlog')
    if not na is None and not nb is None and not nb == na:
        # If the previous username was not the base name
        yield from client.send_message(chatlog, "`NICKNAME CHANGED` " +
                                       str(before) + "\n\tFrom " + nb +
                                       " to " + na)


@client.event
@asyncio.coroutine
def on_member_join(member):
    chatlog = discord.utils.get(member.server.channels, name='chatlog')
    yield from client.send_message(chatlog, "`JOINED` " + str(member))


@client.event
@asyncio.coroutine
def on_member_remove(member):
    chatlog = discord.utils.get(member.server.channels, name='chatlog')
    yield from client.send_message(chatlog, "`LEFT` " + str(member))


@client.event
@asyncio.coroutine
def on_message_delete(message):
    channel = message.channel
    content = message.content.replace('@', '@ ')
    author = message.author
    chatlog = discord.utils.get(message.server.channels, name='chatlog')
    if(str(channel) != 'chatlog'):
        yield from client.send_message(chatlog, "`DELETED` **" + str(channel) +
                                       "**: " + str(author) + ": " +
                                       str(content))


@client.event
@asyncio.coroutine
def on_message_edit(before, after):
    channel = before.channel
    contentb = before.content.replace('@', '@ ')
    contenta = after.content.replace('@', '@ ')
    author = before.author
    chatlog = discord.utils.get(before.server.channels, name='chatlog')
    if(str(channel) != 'chatlog'):
        yield from client.send_message(chatlog, "`EDITTED`\n\t`BEFORE` **" +
                                       str(channel) + "**: " + str(author) +
                                       ": " + str(contentb) +
                                       "\n\tAFTER: " + str(channel) + ": " +
                                       str(author) + ": " + str(contenta))


@client.event
@asyncio.coroutine
def on_message(message):
    admin = discord.utils.get(message.server.roles, name='admin')
    # Logs all messages
    channel = message.channel
    content = message.content.replace('@', '@ ')
    author = message.author
    timestamp = message.timestamp.strftime('%b %d: %H:%M')  # ('%a %b %d: %H:%M:%S')
    chatlog = discord.utils.get(message.server.channels, name='chatlog')
    if(str(channel) != 'chatlog'):
            yield from client.send_message(chatlog, timestamp +
                                           " UTC `SENT` **" + str(channel) +
                                           "**: " + str(author) + ": " +
                                           str(content))

    # Commands
    #Help Commands
    if (str(channel) == 'role-assignment'):
        if message.content.startswith('??roles'):
            yield from client.send_message(message.channel,
                                       "Here is a list of available roles:\n"
                                       "Regions: NA, EUW, EUNE, BR, OCE, CHINA,"
                                       " LAN, LAS, KR, TR, GARENA\nRanks: Bronze, Silver, Gold, "
                                       "Platinum, Diamond+\nRoles: ADC, Support,"
                                       " Mid, Top, Jungle\n")
        elif message.content.startswith('??help'):
            yield from client.send_message(message.channel, "You can add yourself to roles by "
                                  "typing `+!ROLE` and remove yourself with "
                                  "``-!ROLE`. See ??roles for a list of "
                                  "assignable roles. You can also verify your"
                                  " league by using "
                                  "`!verify summonername,region`. Use `??verify`"
                                  " to learn more.")
        elif message.content.startswith('??verify'):
            yield from client.send_message(message.channel, "To verify your account follow these"
                                  "steps:\n1.: Rename your first rune page to"
                                  "'summonersplaza'\n2.: Type `!verify summoner"
                                  "name,region`. Verification is not available "
                                  "for all regions.")
        elif message.content.startswith('??regions'):
            yield from client.send_message(message.channel, "North America = na, "
                                       "EU West = euw, EU North East = eune "
                                       "Latin America North = lan, Latin "
                                       "America South = las, Oceania = oce, "
                                       "Korea = kr, Brazil = br, "
                                       "Turkey = tr, GARENA = garena")
        elif message.content.lower().startswith('+!coach'):
            yield from add_coach(message)
        elif message.content.lower().startswith('-!coach'):
            yield from del_coach(message)

# Roles
        elif message.content.lower().startswith('+!support'):
            yield from add_support(message)
        elif message.content.lower().startswith('+!adc'):
            yield from add_adc(message)
        elif message.content.lower().startswith('+!mid'):
            yield from add_mid(message)
        elif message.content.lower().startswith('+!top'):
            yield from add_top(message)
        elif message.content.lower().startswith('+!jungle'):
            yield from add_jungle(message)
        elif message.content.lower().startswith('-!support'):
            yield from del_support(message)
        elif message.content.lower().startswith('-!adc'):
            yield from del_adc(message)
        elif message.content.lower().startswith('-!mid'):
            yield from del_mid(message)
        elif message.content.lower().startswith('-!top'):
            yield from del_top(message)
        elif message.content.lower().startswith('-!jungle'):
            yield from del_jungle(message)

# Non-verified ranks
        elif message.content.lower().startswith('+!bronze'):
            yield from add_bronze(message)
        elif message.content.lower().startswith('-!bronze'):
            yield from del_bronze(message)
        elif message.content.lower().startswith('+!silver'):
            yield from add_silver(message)
        elif message.content.lower().startswith('-!silver'):
            yield from del_silver(message)
        elif message.content.lower().startswith('+!gold'):
            yield from add_gold(message)
        elif message.content.lower().startswith('-!gold'):
            yield from del_gold(message)
        elif message.content.lower().startswith('+!platinum'):
            yield from add_platinum(message)
        elif message.content.lower().startswith('-!platinum'):
            yield from del_platinum(message)
        elif message.content.lower().startswith('+!diamond+'):
            yield from add_diamondPlus(message)
        elif message.content.lower().startswith('-!diamond+'):
            yield from del_diamondPlus(message)


    # Servers
        elif message.content.lower().startswith('+!euw'):
            yield from add_euw(message)
        elif message.content.lower().startswith('-!euw'):
            yield from del_euw(message)
        elif message.content.lower().startswith('+!na'):
            yield from add_na(message)
        elif message.content.lower().startswith('-!na'):
            yield from del_na(message)
        elif message.content.lower().startswith('+!oce'):
            yield from add_oce(message)
        elif message.content.lower().startswith('-!oce'):
            yield from del_oce(message)
        elif message.content.lower().startswith('+!eune'):
            yield from add_eune(message)
        elif message.content.lower().startswith('-!eune'):
            yield from del_eune(message)
        elif message.content.lower().startswith('+!lan'):
            yield from add_lan(message)
        elif message.content.lower().startswith('-!lan'):
            yield from del_lan(message)
        elif message.content.lower().startswith('+!br'):
            yield from add_brazil(message)
        elif message.content.lower().startswith('-!br'):
            yield from del_brazil(message)
        elif message.content.lower().startswith('+!china'):
            yield from add_china(message)
        elif message.content.lower().startswith('-!china'):
            yield from del_china(message)
        elif message.content.lower().startswith('+!las'):
            yield from add_lan(message)
        elif message.content.lower().startswith('-!las'):
            yield from del_lan(message)
        elif message.content.lower().startswith('+!kr'):
            yield from add_lan(message)
        elif message.content.lower().startswith('-!kr'):
            yield from del_lan(message)
        elif message.content.lower().startswith('+!turkey'):
            yield from add_lan(message)
        elif message.content.lower().startswith('-!turkey'):
            yield from del_lan(message)
        elif message.content.lower().startswith('+!garena'):
            yield from add_lan(message)
        elif message.content.lower().startswith('-!garena'):
            yield from del_lan(message)
    # Update/link account
        elif message.content.startswith('!verify'):
            yield from verify(message)
    # Admin Commands
        elif message.content.startswith('!savelogs'):
            if admin in message.author.roles or Moderator in message.author.roles:
                logs = yield from savelogs(message)
                if logs == "":
                    yield from client.send_message(message.channel, "The number you input was invalid, or some other error occured. Use the format !savelogs ChannelName NumberOfMessages")
                else:
                    print(logs)
                    #Hello merK
                    #The string S is a string with all the relevent chatlogs in order, broken apart by new line characters
                    #If you instead want the raw list, use the method savelogs2 instead
            else:
                yield from client.send_message(message.channel, "You are not an admin. Who do you think you are fooling? You think I'll stand for this? I will.")

client.run(id.token1())
#client.run('MjA3NjI3MzczNjc0MzY0OTI4.CoYx5g.oKRKeZFXWah9hlTlq3qk7gCJE28')