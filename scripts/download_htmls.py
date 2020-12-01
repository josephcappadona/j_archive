from sys import argv
from pathlib import Path
from j_archive.htmls import download_htmls, write_htmls
from j_archive.utils import make_archive


if __name__ == '__main__':

    DATA_DIR = Path(argv[1] if len(argv) > 1 else 'data')
    LIMIT = int(argv[2]) if len(argv) > 2 else None

    htmls = download_htmls(limit=LIMIT)
    write_htmls(htmls, data_dir=DATA_DIR, verbose=True)