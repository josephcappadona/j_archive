from sys import argv
from pathlib import Path
from j_archive.htmls import read_htmls
from j_archive.clues import parse_clues, write_clues
from j_archive.utils import make_archive


if __name__ == '__main__':

    DATA_DIR = Path(argv[1] if len(argv) > 1 else 'data')

    clues = parse_clues(read_htmls(data_dir=DATA_DIR))
    write_clues(clues, data_dir=DATA_DIR, verbose=True)