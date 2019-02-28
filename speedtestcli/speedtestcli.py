import io
from datetime import datetime

import requests
import speedtest
from telethon import events

from tg_companion.tgclient import client



SPEEDTEST_HELP = """
    **Test your internet speed using http://speedtest.net/**
"""

@client.CommandHandler(outgoing=True, command="speedtest", help=SPEEDTEST_HELP)
async def run_speedtest(e):
    await e.edit("`Calculating your internet speed. Please wait!`")
    chat = await e.get_chat()

    start_time = datetime.now()

    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end_time = start_time - datetime.now()
    offset = end_time.seconds + (end_time.days * 60 * 60 * 24)
    seconds = offset % 60

    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    try:
        response = requests.get(s.results.share())

        with io.BytesIO(response.content) as speedtest_image:
            speedtest_image.name = "speedtest.png"
            await e.edit(f"Speedtest collected in {seconds}s")
            await client.send_file(chat.id, speedtest_image, caption=f"Here are your speed test results", reply_to=e)

    except (speedtest.ShareResultsConnectFailure, speedtest.ShareResultsSubmitFailure) as exc:
        print(type(exc))
        await e.edit(f"__Download:__ `{convert_from_bytes(download_speed)}`"
                     f"\n__Upload:__ `{convert_from_bytes(upload_speed)}`"
                     f"\n__Ping:__ `{ping_time}`"
                     f"\nCollected in: `{seconds}s`")


def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {
        0: '',
        1: 'kilobytes',
        2: 'megabytes',
        3: 'gigabytes',
        4: 'terabytes'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"
