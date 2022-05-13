
from pathlib import Path


def create_folder(foldername):
    ''' creates folder if it does not exists'''
    Path(foldername).mkdir(parents=True, exist_ok=True)
