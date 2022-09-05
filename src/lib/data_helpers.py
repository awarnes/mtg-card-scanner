import json
import os
import re

from collections import defaultdict

DEFAULT_CARD_DATA = '/Users/alexanderwarnes/code/mtg-card-scanner/test/mtg-cards/AtomicCards.json'
DEFAULT_TEST_FOLDER = '/Users/alexanderwarnes/code/mtg-card-scanner/test'
SUPPORTED_MOVIE_FORMATS = ('.mp4', '.mov', '.avi', '.flv', '.wmv')

def get_card_data(card_data_path=DEFAULT_CARD_DATA):
    choice_data = []

    with open(card_data_path) as card_data:
        data = json.load(card_data)
        choice_data += data['data'].keys()

    match_choices = defaultdict(list)
    for choice in choice_data:
        if re.match(r'[1_\+"a]', choice[0].lower()):
            match_choices['a'].append(choice)
        else:
            match_choices[choice[0].lower()].append(choice)
    
    return match_choices

def get_test_movie_path(name, path=DEFAULT_TEST_FOLDER):
    if name:
        return os.path.join(path, f"{name}.mov")
    
    options = []

    for file in os.listdir(path):
        if file.endswith(SUPPORTED_MOVIE_FORMATS):
            options.append(os.path.join(path, file))
    
    return options