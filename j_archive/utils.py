import os
import shutil
import requests
from pathlib import Path
from zipfile import ZipFile

__all__ = ['make_archive', 'unzip_archive', 'download_htmls_gdrive', 'download_clues_gdrive']


def make_archive(source, destination):
    # adapted from https://stackoverflow.com/a/61596253
    source = str(Path(source).resolve())
    destination = str(Path(destination).resolve())
    base_name = '.'.join(destination.split('.')[:-1])
    format = destination.split('.')[-1]
    root_dir = os.path.dirname(source)
    base_dir = os.path.basename(source.strip(os.sep))
    shutil.make_archive(base_name, format, root_dir, base_dir)

def unzip_archive(zip_filepath, verbose=True):
    zip_filepath = Path(zip_filepath)
    with ZipFile(zip_filepath, 'r') as zip_ref:
        if verbose:
            print(f'Unzipping {str(zip_filepath)}...')
        zip_ref.extractall(zip_filepath.parent)

HTMLS_GDRIVE_ID = '1CIn5TwFE9zaxPXe6HGvjUKdANT7kr2rN'
def download_htmls_gdrive(data_dir='data', overwrite=False, verbose=True):
    data_dir = Path(data_dir)
    html_zip_filepath = data_dir / 'html.zip'
    html_dir = data_dir / 'html'

    if not html_dir.exists() or overwrite:
        print(f"Downloading HTML data from Google Drive...")
        os.makedirs(html_dir)
        download_gdrive(HTMLS_GDRIVE_ID, html_zip_filepath)
        unzip_archive(html_zip_filepath, verbose=verbose)
        os.remove(html_zip_filepath)
    else:
        print(f"HTML data already exists. To redownload, pass `overwrite=True`.")

CLUES_GDRIVE_ID = '1P3oKIdfvcwcQh-D8yIqR4Ufmjl9Iew5L'
def download_clues_gdrive(data_dir='data', overwrite=False, verbose=True):
    data_dir = Path(data_dir)
    clues_zip_filepath = data_dir / 'clues.zip'
    clues_dir = data_dir / 'clues'

    if not clues_dir.exists() or overwrite:
        print(f"Downloading clue data from Google Drive...")
        os.makedirs(clues_dir)
        download_gdrive(CLUES_GDRIVE_ID, clues_zip_filepath)
        unzip_archive(clues_zip_filepath, verbose=verbose)
        os.remove(clues_zip_filepath)
    else:
        print(f"Clue data already exists. To redownload, pass `overwrite=True`.")

def download_gdrive(id, destination):
    # adapted from https://stackoverflow.com/a/39225272

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)