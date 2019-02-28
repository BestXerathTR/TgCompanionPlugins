import aiohttp

from tg_companion.tgclient import client

PASTE_HELP = """
    **Paste a text to del.dog**
    __Usage:__
        Reply to a text message
        or use the command followed by a text.
    __Args:__
        `<text>` - **(required if not reply)** __Text to paste on del.dog__
"""

GET_PASTE_HELP = """
    **Get the content of a paste**
    __Args:__ **(required)** - __The url from the paste command__
"""

URL = "https://del.dog"


@client.CommandHandler(
        outgoing=True,
        command=".paste",
        func=lambda e: True if e.reply_to_msg_id else False, help=PASTE_HELP)
async def reply_paste(event):
    reply_to = await event.get_reply_message()

    content = reply_to.message

    if content:
        await event.edit(f"`Sending content to {URL}`")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{URL}/documents", data=content.encode("utf-8")) as request:
                if request.status == 404:
                    await event.edit("`Failed to connect to dogbin`")
                    return
                response = await request.json()

                if request.status != 200:
                    dogbin_error = response.get("message")
                    await event.edit(f"__There was an error while connecting to dogbin__: `{dogbin_error}`")
                    return

                paste_key = response.get("key")
                await event.edit(f"__Here is paste:__ {URL}/{paste_key}")

    else:
        await event.edit("`There's no text to paste`")


@client.CommandHandler(
        outgoing=True,
        command=r".paste ([\s\S]+)",
        func=lambda e: False if e.reply_to_msg_id else True)
async def paste(event):

    content = event.pattern_match.group(1)

    if content:
        await event.edit(f"`Sending content to {URL}`")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{URL}/documents", data=content.encode("utf-8")) as request:
                if request.status == 404:
                    await event.edit("`Failed to connect to dogbin`")
                    return
                response = await request.json()

                if request.status != 200:
                    dogbin_error = response.get("message")
                    await event.edit(f"__There was an error while connecting to dogbin__: `{dogbin_error}`")
                    return

                paste_key = response.get("key")
                await event.edit(f"__Here is paste:__ {URL}/{paste_key}")

    else:
        await event.edit("`There's no text to paste`")


@client.CommandHandler(outgoing=True, command=".getpaste (.+)", help=GET_PASTE_HELP)
async def get_paste(event):
    paste_key = event.pattern_match.group(1).rsplit('/', 1)[-1]

    await event.edit(f"`Downloading the raw content from {paste_key}`")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}/raw/{paste_key}") as request:
            if request.status != 200:
                if request.status == 404:
                    await event.edit("`Failed to connect to dogbin`")
                    return
                elif request.stats != 200:
                    await event.edit("`Unknown error occured`")
                    return

                response = await request.json()
                dogbin_error = response.get("message")
                await event.edit(f"__There was an error while connecting to dogbin__: `{dogbin_error}`")
                return

            content = await request.text()
            await event.edit(f"`{content}`")
