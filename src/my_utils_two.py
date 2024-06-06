""" Utility functions for podcast scraper."""

from __future__ import annotations
from collections.abc import Iterable

from requests import Session
from requests.exceptions import RequestException

# from lxml import html


def write_mp3(tracks: Iterable, link: str) -> None:
    """Write mp3 to disk."""
    for track in tracks:
        with open(f'{track}.mp3', 'wb') as podcast:
            with Session() as session:
                a_file = session.get(link, timeout=30)
                podcast.write(a_file.content)
                print(f'{track} Downloaded')


def write_xml(xml_page: str, file_name: str = "pdc_rec") -> None:
    """Store xml page on disk"""
    with open(f'{file_name}.xml', 'wb') as page:
        page.write(xml_page)


def request_xml(page: str) -> str | None:
    """Get xml page."""
    with Session as session:
        try:
            page = session.get(page)
            return page.text
        except RequestException as e:
            print(f'Unable to connect to page. {e}')
            return None
