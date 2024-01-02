import subprocess
import time
import re

from . import common
from .models import Channel, Video, migrate
from .youtube_api import ChannelNotFoundError
from datetime import datetime
from icecream import ic
from .tasks import huey
from .common import download_preview_immediate, download_video_thumbnail, download_video_thumbnails, convert_iso8601
import asyncio
from . import video_fetch_generator

huey.immediate = True

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

# http://localhost:8080/channel/UCYn9o7_fFhLsIYBlU7_MPGg


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



def reencode_preview():
    channels = list(Channel.select())
    # prioritize your favorite channels
    channels.sort(key=lambda c: c.num_local_videos(), reverse=True)
    for channel in channels:
        videos = list(channel.videos())
        for v in videos:
            try:
                file_path = v.file_path()
            except Exception:
                continue
            try:
                v.preview_file_path()
            except Exception:
                v.reencode_preview()


def download_preview_videos():

    #channels = list(Channel.select().order_by(Channel.local_view_count.desc()))
    # for channel in channels:
    #     videos = list(channel.videos())[:10]
    #     #cutoff = datetime(year=2023, month=8, day=1)
    videos = list(Video.select().order_by(Video.published_at.desc()))
    for v in videos:
        v: Video
        if v.preview_file_path().exists():
            continue

        print('///////////////looking for', v, v.published_at, v.channel)
        try:
            v.download_preview_shorter()
        except subprocess.CalledProcessError as exc:
            pass
            # if downloaded:
            #     print('@@@@@@@@@@@@@download failed, re-encoding', v, v.channel)
            #     v.reencode_preview()


#print(convert_iso8601('PT1H1M1S'))
migrate()

