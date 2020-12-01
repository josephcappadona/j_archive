# J-Archive Dataset

## Usage

Install this library:

```bash
python3 -m pip install https://github.com/josephcappadona/j_archive.git
```

Run the following in python:

```python
import j_archive

clues = j_archive.read_clues()  # returns a generator
for clue in clues:
    # do something
```

The first time you attempt to load clues, the library will download the clues data from Google Drive. If you wish to do this explicitly, you can run `j_archive.download_clues_gdrive()`.

## Building from scratch

If you wish to redownload the HTMLs and reparse the clue data from scratch, you can do so with the following scripts:

```bash
python3 scripts/download_htmls.py [DATA_DIR] [LIMIT]
python3 scripts/extract_clues.py [DATA_DIR]
```

Note that if you pass anything other than the default of `data` in for `DATA_DIR`, then you will need to pass the same directory into `j_archive.read_clues` when loading the clue data, e.g., `j_archive.read_clues(data_dir='my_custom_dir')`. The `LIMIT` parameter is useful for testing purposes.