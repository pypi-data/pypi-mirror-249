import subprocess
import time
import re

from . import common
from .models import Channel, Video, migrate
from .youtube_api import ChannelNotFoundError
from datetime import datetime
from icecream import ic
from .common import download_video_thumbnail, download_video_thumbnails, convert_iso8601
from ytcl.tasks import download_preview
import asyncio
from . import video_fetch_generator


"""
"""

async def video_fetch_generator_all(*args, **kwargs):
    i = 0
    async for ele in video_fetch_generator(*args, **kwargs):
        if i % 50 == 0:
            print(i)
        i += 1


def download_all_channels():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    for channel in Channel.select():
        if channel.num_videos() == 0:
            print(channel.id, channel.name)
            asyncio.run(video_fetch_generator_all([channel], downloaded_ytids=[], first_page_only=False))
            time.sleep(60 * 30)


#download_all_channels()

def download_missing_video_thumbnails():
    ytids_with_thumbnails = set(p.stem for p in common.THUMBNAILS_ROOT.glob('**/*.jpg'))
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #download_video_thumbnail(ytid, outpath: Path, session: ClientSession):
    for channel in Channel.select():
        ytids = []
        for v in Video.select(Video.ytid).where(Video.channel == channel):
            if v.ytid not in ytids_with_thumbnails:
                ytids.append(v.ytid)
                # get the full object
        print('downloading', len(ytids), 'thumbnails')
        asyncio.run(download_video_thumbnails(channel_id=channel.id, ytids=ytids))

#download_missing_video_thumbnails()



def populate_thumbnails():
    for c in Channel.select():
        c: Channel

        if not c.thumbnail_file_path().exists():
            print('updating data for', c)
            try:
                c.update_from_api()
            except ChannelNotFoundError:
                pass
            else:
                c.download_thumbnail()


def measure_size():
    dims = []
    for v in Video.select():
        w = v.width
        h = v.height
        if w > h:
            h, w = w, h
        dims.append((w, h))
    from collections import Counter
    c = Counter(dims)
    for ((w, h), count) in c.most_common():
        divisible_by = []
        for i in range(1, 11):
            if not (w % i or h % i):
                divisible_by.append(i)






#print(convert_iso8601('PT1H1M1S'))
migrate()

