from nose.tools import with_setup
from spellchecker import *
import json


def setup_func():
    dictionary = open('../../../../../usr/share/dict/words').read().split()
    SIZE = len(dictionary) - 1
    json_data = open('wordlist.json')
    wordlist = json.load(json_data) 
    json_data.close()

    
@with_setup(setup_func)
def test_check_frequencies():
    assert check_frequencies(['weka', 'weki', 'woke', 'waka', 'wake']) == 'wake' 
    assert check_frequencies(['sheep', 'shoop', 'shaup', 'shop', 'shap', 'ship']) == 'sheep'
    assert check_frequencies(['popple', 'people']) == 'people'


@with_setup(setup_func)
def test_word_search():
    assert word_search(dictionary, 'weke', 0, SIZE) == None
    assert word_search(dictionary, 'conspiracy', 0, SIZE) == 'conspiracy'


def test_replace_vowels():
    assert len(replace_vowels('rendition', [], 0)) == 5**4 
    assert len(replace_vowels('cunsperricy', [], 0)) == 5**3
    assert len(replace_vowels('weke', [], 0)) == 5**2
    assert len(replace_vowels('job', [], 0)) == 5**1


def test_remove_duplicates():
    assert sorted(remove_duplicates('sheeeeep')) == ['sheeeep', 'sheeep', 'sheep', 'shep']


@with_setup(setup_func)
def test_spellcheck():
    assert spellcheck('jjoobbb') == 'job'
    assert spellcheck('cunsperricy') == 'conspiracy'
    assert spellcheck('sheeeeep') == 'sheep'
    assert spellcheck('weke') == 'wake'
    assert spellcheck('sheeple') == 'NO SUGGESTION'
