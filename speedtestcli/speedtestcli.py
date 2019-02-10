from tg_companion.tgclient import client
from telethon import events
import speedtest


@client.on(events.NewMessage(outgoing=True, pattern=r"\.speedtest"))
async def run_speedtest(e):
    await e.edit("`Calculating your internet speed. Please wait!`")

    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()

    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    await e.edit(f"__Download:__ `{convert_from_bytes(download_speed)}`"
                 f"\n__Upload:__ `{convert_from_bytes(upload_speed)}`"
                 f"\nPing: {ping_time}")


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
