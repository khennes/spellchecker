# This program takes a correctly spelled English word as input and generates 
# a misspelled version of it (with duplicate letters and mixed-up vowels),
# which is then piped into spellchecker.py to test that the spell checker 
# always returns a valid word.

import re
import random
import spellchecker

dictionary = open('../../../../../usr/share/dict/words').read().split()
SIZE = len(dictionary) - 1

def spellchecker_test():

    while True:
        word = raw_input("> ").strip().lower()

        # validate user input
        if spellchecker.word_search(dictionary, word, 0, SIZE) is None:
            print "Please enter a valid word."
            continue
        
        misspelling = add_duplicates(replace_vowels(word))
        print "%s => %s" % (misspelling, spellchecker.spellcheck(misspelling))

        continue


def replace_vowels(word):
    mixed_vowels = { 'a': 'o', 'e': 'u', 'i': 'a', 'o': 'e', 'u': 'i' } 
    for char in word:
        if char in 'aeiou':
            word = word.replace(char, mixed_vowels[char], 1)

    return word


def add_duplicates(word):
    letters = random.sample(word, len(word)/2)
    for char in word:
        if char in letters:
            index = word.index(char)
            word = word[:index + 1] + char + word[index + 1:]

    return word



if __name__ == "__main__":
    spellchecker_test()
