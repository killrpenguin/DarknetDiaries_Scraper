"""
The library object handles the gathering and tracking of Darknet Diary Podcast
episodes locally and on the net
"""
from __future__ import annotations
import os
from os.path import expanduser
from lxml import html
from requests import Session
from requests import Response
from requests.exceptions import RequestException


class Library:
    """TODO Describe Class"""

    def __init__(self) -> None:
        """TODO describe function
        :returns: None
        """
        if self._dn_page is not None:
            self.tree = html.document_fromstring(self._dn_page.content)

    def __repr__(self) -> str:
        return f'{type(self).__name__}'

    def __str__(self) -> str:
        return 'Darknet Diaries Library'

    @property
    def _dn_page(self) -> Response | None:
        try:
            with Session() as session:
                dn_request = session.get(
                    'https://feeds.megaphone.fm/darknetdiaries', timeout=30)
        except RequestException:
            return None
        return dn_request

    @property
    def local_files(self) -> dict[int, str]:
        """TODO Describe function
        :returns: dict[int, string]
        """
        file_names = os.listdir(expanduser('~/Music/Darknet_Diaries_Podcasts'))
        loc_files_hmap = {
            k: v
            for k, v in zip(range(len(file_names)), file_names) if ' -' in v
        }
        return loc_files_hmap

    @property
    def dn_names(self) -> list[str]:
        """TODO Describe functio
        """
        if self._dn_page is not None:
            names = [
                element.text for element in self.tree.xpath('//title')
                if 'Darknet Diaries' not in element.text
            ]
            names = [
                name.replace(':', ' -').replace('"', '').strip('Ep ')
                for name in names
            ]
        return names

    @property
    def dn_links(self) -> list[str]:
        """TODO Describr class

        """
        if self._dn_page is not None:
            links = self.tree.xpath('//enclosure[contains(@url,"mp3")]/@url')
        return links

    def get_them_all(self) -> None:
        """TODO Describe function
        """
        if self.dn_names is not None and self.dn_links is not None:
            if len(self.dn_names) == len(self.dn_links):

                for (track, link) in zip(self.dn_names, self.dn_links):
                    if track not in self.local_files.values():

                        with open(f'{track}.mp3', 'wb') as podcast:
                            with Session() as session:
                                a_file = session.get(link, timeout=30)
                                podcast.write(a_file.content)
                                print(f'{track} Downloaded')
