from __future__ import annotations
from asyncio import Queue as aQueue
from asyncio import BoundedSemaphore
from asyncio import QueueEmpty
from asyncio import sleep
from asyncio import gather
from collections.abc import Mapping
from collections.abc import Iterable

from aiofile import async_open
from aiohttp import ClientSession
from aiohttp import TCPConnector
from requests import Session

from podcast import Podcast
from podcast import Podcasts


class DownloadTool:
    """ Asynchronously download the Darknet Diaries Podcasts.
    """

    def __init__(self) -> None:
        self._max_dls: int = 5
        self._podcasts: Podcasts = Podcasts()
        self._dl_queue: aQueue = aQueue(maxsize=self._max_dls)
        self._semaphore: BoundedSemaphore = BoundedSemaphore(self._max_dls)
        self._tcp_connection: TCPConnector = TCPConnector(limit=25)
        self._header: Mapping = {"Authorization": "Basic bG9naW46cGFzcw=="}
        self._dl = None

    def __repr__(self) -> str:
        return f'{type(self).__name__}()'

    def __str__(self) -> str:
        return 'Download Tool'

    async def _dl_podcast(self, session: ClientSession) -> None:
        for podcast in self._podcasts.values():
            async with self._semaphore:
                async with session.get(podcast.dl_link, ssl=False,
                                       timeout=600) as resp:
                    assert resp.status < 299
                    print(f'Downloading: {podcast.title}')
                    mp3 = await resp.read()
                async with async_open(f'{podcast.ep_num}-{podcast.title}.mp3',
                                      "wb") as file:    # look up "wb"
                    await file.write(mp3)
        await self._dl_queue.put(None)

    async def _manage_queue(self) -> None:
        while True:
            try:
                self._dl = self._dl_queue.get_nowait()
            except QueueEmpty:
                await sleep(0.5)
            if self._dl is None:
                break

    async def dl_all_podcasts(self) -> None:
        async with ClientSession(connector=self._tcp_connection,
                                 headers=self._header,
                                 trust_env=True) as session:
            await gather(self._dl_podcast(session), self._manage_queue())

    def dl_podcasts(self, selected: Iterable[Podcast]) -> None:
        with Session() as session:
            for podcast in selected:
                dl = session.get(self._podcasts[podcast])
                with open(f'{podcast.ep_num}-{podcast.title}.mp3',
                          'wb') as file:
                    file.write(dl.content)
