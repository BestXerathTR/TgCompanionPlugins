from tg_companion.tgclient import client
import emoji
import random
import re
import urllib
import bs4
import aiohttp



COPY_PASTA_HELP = """
    **Replace random characters in a text with random emojis**
    __Usage:__
        __Reply to a message or use the command followed by a text__
"""


OWO_HELP = """
    **Translates a text in owo cuteness**
    __Usage:__
        __Reply to a message or use the command followed by a text__
"""
GANGSTAFY_HELP = """
    **Makes any text look like it was written by Snoop Dogg**
    __Usage:__
        __Reply to a message or use the command followed by a text__
"""

REVERSE_HELP = """
    **Reverse any given text**
    __Usage:__
        __Reply to a message or use the command followed by a text__
"""

VAPOR_HELP = """
    **Convert normal text to vaporwave font style text**
    __Usage:__
        __Reply to a message or use the command followed by a text__
"""

@client.CommandHandler(outgoing=True, command="copypasta", help=COPY_PASTA_HELP)
async def copypasta(event):
    message = None
    split_text = event.text.split(None, 1)
    if event.reply_to_msg_id:
        rep_msg = await event.get_reply_message()
        message = rep_msg.text
    elif len(split_text) == 1:
        await client.update_message(event, "...")
        return

    elif not message:
        await client.update_message(event, "`Unsuported message`")
        return
    else:
        message = split_text[1]

    emojis = emojis = ["😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
    reply_text = random.choice(emojis)
    rand_char = random.choice(message)

    for char in message:
        if char == " ":
            reply_text += random.choice(emojis)
        elif char in emojis:
            reply_text += char + random.choice(emojis)
        elif char.lower() == rand_char:
            reply_text += "🅱️"
        else:
            if bool(random.getrandbits(1)):
                reply_text += char.upper()
            else:
                reply_text += char.lower()
        reply_text += random.choice(emojis)
    await client.update_message(event, reply_text)

@client.CommandHandler(outgoing=True, command="owo", help=OWO_HELP)
async def owo(event):
    message = None
    split_text = event.text.split(None, 1)
    if event.reply_to_msg_id:
        rep_msg = await event.get_reply_message()
        message = rep_msg.text
    elif len(split_text) == 1:
        await client.update_message(event, "...")
        return

    elif not message:
        await client.update_message(event, "`Unsuported message`")
        return
    else:
        message = split_text[1]
    faces = ['(・`ω´・)',';;w;;','owo','UwU','>w<','^w^','\(^o\) (/o^)/','( ^ _ ^)∠☆','(ô_ô)','~:o',';____;', '(*^*)', '(>_', '(♥_♥)', '*(^O^)*', '((+_+))']

    reply_text = re.sub(r'r|l', "w", message)
    reply_text = re.sub(r'R|L', 'W', reply_text)
    reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
    reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
    reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
    reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
    reply_text += ' ' + random.choice(faces)

    await client.update_message(event, reply_text)


@client.CommandHandler(outgoing=True, command="gangstafy", help=GANGSTAFY_HELP)
async def gangstafy_text(event):
    message = None
    split_text = event.text.split(None, 1)
    if event.reply_to_msg_id:
        rep_msg = await event.get_reply_message()
        message = rep_msg.text
    elif len(split_text) == 1:
        await client.update_message(event, "...")
        return

    elif not message:
        await client.update_message(event, "`Unsuported message`")
        return
    else:
        message = split_text[1]
    await client.update_message(event, await __gangsafy(message))


@client.CommandHandler(outgoing=True, command="reverse", help=REVERSE_HELP)
async def reverse_text(event):
    message = None
    split_text = event.text.split(None, 1)
    if event.reply_to_msg_id:
        rep_msg = await event.get_reply_message()
        message = rep_msg.text
    elif len(split_text) == 1:
        await client.update_message(event, "...")
        return

    elif not message:
        await client.update_message(event, "`Unsuported message`")
        return
    else:
        message = split_text[1]
    await client.update_message(event, message[::-1])


@client.CommandHandler(outgoing=True, command="vapor", help=VAPOR_HELP)
async def vapor_text(event):
    message = None
    split_text = event.text.split(None, 1)
    if event.reply_to_msg_id:
        rep_msg = await event.get_reply_message()
        message = rep_msg.text
    elif len(split_text) == 1:
        await client.update_message(event, "...")
        return

    elif not message:
        await client.update_message(event, "`Unsuported message`")
        return
    else:
        message = split_text[1]

    WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
    WIDE_MAP[0x20] = 0x3000
    await client.update_message(event, message.translate(WIDE_MAP))



# Function helpers:

async def __gangsafy(text):
    urls = ("http", "www.", "https")
    if text.startswith(urls):
        params = {"search": __remove_emojis(text)}
        return "http://www.gizoogle.net/tranzizzle.php?{}".format(urllib.parse.urlencode(params))
    params = {"translatetext": __remove_emojis(text)}
    target_url = "http://www.gizoogle.net/textilizer.php"
    async with aiohttp.ClientSession() as session:
        async with session.post(target_url, data=params) as response:
            soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', await response.text())
    soup = bs4.BeautifulSoup(soup_input, "lxml")
    giz = soup.find_all(text=True)
    giz_text = giz[39].strip("\r\n")
    return giz_text

def __remove_emojis(text):
    clean_text = text
    for char in text:
        if char in list(emoji.EMOJI_UNICODE.values()):
            clean_text = re.sub(char, "", clean_text)
    return clean_text
