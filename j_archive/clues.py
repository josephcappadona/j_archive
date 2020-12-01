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

from .utils import download_clues_gdrive

__all__ = ['parse_clues', 'write_clues', 'read_clues']


def parse_clue(clue_div):
    clue = {}

    clue_text_div = clue_div.find('td', {'class': 'clue_text'})
    clue['text'] = clue_text_div.text
    clue['id'] = clue_text_div.get('id')
    
    onmouseover = clue_div.find('table').find('tr').find('td').find('div').get('onmouseover')
    answer_soup = BeautifulSoup(onmouseover, 'html.parser')
    answer = answer_soup.find('em').text
    clue['answer'] = answer
    
    return clue

def parse_FJ_clue(final_round_div):
    clue = {}
    clue_text_div = final_round_div.find('td', {'class': 'clue_text'})
    clue['text'] = clue_text_div.text
    clue['id'] = clue_text_div.get('id')

    clue['category'] = unescape(final_round_div.find('td', {'class': 'category'}).find('td', {'class': 'category_name'}).text)

    onmouseover = final_round_div.find('tr').find('td').find('div').get('onmouseover')
    answer_soup = BeautifulSoup(onmouseover, 'html.parser')
    answer = answer_soup.find('em').text
    clue['answer'] = answer

    return clue

def parse_game_html(html, game_id):
    soup = BeautifulSoup(html, 'html.parser')

    categories = []
    round_divs = soup.find_all('table', {'class': 'round'})
    for round_div in round_divs:
        category_divs = round_div.find_all('td', {'class': 'category'})
        round_categories = []
        for category_div in category_divs:
            category_name = unescape(category_div.find('td', {'class': 'category_name'}).text)
            round_categories.append(category_name)
        categories.append(round_categories)

    final_round_div = soup.find('table', {'class': 'final_round'})
    final_round_div_copy = copy.copy(final_round_div)
    try:
        final_round_div.decompose()
    except:
        pass

    clue_divs = soup.find_all('td', {'class': 'clue'})
    clues = []
    for clue_div in clue_divs:
        try:
            clue = parse_clue(clue_div)

            clue_id_split = clue['id'].split('_')
            col, row = map(int, clue_id_split[-2:])
            round = clue_id_split[-3]
            round_num = 1 if round == 'J' else 2
            category = categories[round_num - 1][col - 1]
            value = 200 * row * round_num
            
            clue['game_id'] = game_id
            clue['id'] = clue['id'].replace('clue', str(game_id))
            clue['round'] = round
            clue['category'] = category
            clue['value'] = value
            clues.append(clue)
        except:
            pass

    try:
        FJ_clue = parse_FJ_clue(final_round_div_copy)
        FJ_clue['game_id'] = game_id
        FJ_clue['id'] = FJ_clue['id'].replace('clue', str(game_id))
        clues.append(FJ_clue)
    except:
        pass

    return clues

def parse_clues(htmls, verbose=False):
    for html_filepath, html in htmls:
        if verbose:
            print(f'Parsing {html_filepath}')
        game_id = int(Path(html_filepath).stem)
        game_clues = parse_game_html(html, game_id)
        for clue in game_clues:
            yield clue

def write_clues(clues, data_dir='data', overwrite=True, verbose=False):
    data_dir = Path(data_dir)
    clues_dir = data_dir / 'clues'
    os.makedirs(clues_dir, exist_ok=True)

    for clue in clues:
        clue_filepath = clues_dir / f"{clue['id']}.json"
        if not clue_filepath.exists() or overwrite:
            with open(clue_filepath, 'w+') as f:
                json.dump(clue, f)
                if verbose:
                    print(f'Wrote {str(clue_filepath)}')

def read_clues(data_dir='data'):
    data_dir = Path(data_dir)
    clues_dir = data_dir / 'clues'

    clues_query = str(clues_dir / '*.json')
    clues_filepaths = sorted(glob(clues_query))

    if not clues_filepaths:
        download_clues_gdrive(data_dir=data_dir)
        clues_filepaths = sorted(glob(clues_query))

    def _generator():
        for clue_filepath in clues_filepaths:
            with open(clue_filepath) as f:
                yield json.load(f)
    return _generator()
