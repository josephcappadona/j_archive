import os
import re
import copy
import json
import shutil
from urllib.request import urlopen
from pathlib import Path
from glob2 import glob
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape

from .utils import unzip_archive, download_htmls_gdrive

__all__ = ['download_htmls', 'write_htmls', 'read_htmls']


def download_htmls(max_=6880, limit=None, verbose=False):
    count = 0
    for game_id in range(1, max_+1):
        url = f'http://www.j-archive.com/showgame.php?game_id={game_id}'
        if verbose:
            print(f'Downloading {url}')
        resource = urlopen(url)
        html = resource.read().decode(resource.headers.get_content_charset())
        yield game_id, html
        count += 1
        if limit and count >= limit:
            break

def write_htmls(htmls, data_dir='data', overwrite=True, verbose=False):
    data_dir = Path(data_dir)
    htmls_dir = data_dir / 'html'
    os.makedirs(htmls_dir, exist_ok=True)

    for game_id, html in htmls:
        html_filepath = htmls_dir / f'{game_id}.html'
        if not html_filepath.exists() or overwrite:
            with open(html_filepath, 'w+') as f:
                f.write(html)
                if verbose:
                    print(f'Wrote {str(html_filepath)}')

def read_htmls(data_dir='data', download=False, limit=None):
    data_dir = Path(data_dir)
    html_dir = data_dir / 'html'

    html_query = str(html_dir / '*.html')
    html_filepaths = sorted(glob(html_query))
    if not html_filepaths:
        if download:
            download_htmls_gdrive(data_dir=data_dir)
        else:
            raise ValueError(f"Couldn't find HTMLs in {str(html_dir)}. To download them from Google Drive, pass `download=True`.")

    for html_filepath in html_filepaths:
        with open(html_filepath) as f:
            yield html_filepath, f.read()