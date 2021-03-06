# This program takes a single word from the user as input and searches for it
# inside a large list of valid English words. If the input word does not exist, 
# the program generates many permutations of the original word, by removing
# duplicate characters and swapping out vowels, and returns the closest valid match.

import re
import json


### GLOBALS ###

# Load list of valid English words
dictionary = open('../../../../../usr/share/dict/words').read().split()
SIZE = len(dictionary) - 1

# Load JSON file of 10,000 most common English words, scraped from: 
# https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/1-10000
json_data = open('wordlist.json')
wordlist = json.load(json_data) 
json_data.close()

### End Globals ###


def main():
    while True:
        input = raw_input("> ").strip().lower()
        word = ''.join(re.findall('[a-zA-Z-]', input))
        print spellcheck(word) 


def spellcheck(word):

    # look up input word, print and return if valid
    result = word_search(dictionary, word, 0, SIZE)
    if result is not None:
        return result

    # otherwise, generate list of alternatives
    else:
        replaces = replace_vowels(word, [], 0)
        removals = remove_duplicates(word)

        for removal in removals:
            replaces += replace_vowels(removal, [], 0)

        edits = removals + replaces

        suggestions = []
        for edit in edits:
            result = word_search(dictionary, edit, 0, SIZE)
            if result is not None and result not in suggestions:
                suggestions.append(result)

        if suggestions == []:
            return "NO SUGGESTION"
        elif len(suggestions) == 1:
            return suggestions[0]
        else:
            return check_frequencies(suggestions)


# Scan input word for vowels and output a list of possible permutations
# (the length of the output list will always be 5**n, where n is the number of
# vowels in the word).
# Then, recursively perform the same operation on each possible permutation 
# of the original word, until the end of the word is reached.

def replace_vowels(word, replaces, i):
    if i > len(word) - 1:
        return

    new_words = []
    if word[i] in 'aeiou':
        new_words = [ word[i:].replace(word[i], v, 1) for v in 'aeiou' ]
        for new_word in new_words:
            new_word = word[:i] + new_word
            if new_word not in replaces:
                replaces.append(new_word)
            replace_vowels(new_word, replaces, i + 1)
        
    else:
        replace_vowels(word, replaces, i + 1)

    return list(set(replaces))


# Using Norvig's list comprehension strategy, scan the input word for duplicates
# and generate a list of new strings with the duplicates removed. If necessary, 
# recursively scan the word again to catch chains of duplicates > 2.

def remove_duplicates(word):
    splits = [ (word[:i], word[i:]) for i in range(len(word) + 1) ] 
    removals = [ a + b[1:] for a, b in splits if a and b and a[-1] == b[0] ]

    if removals is not None:
        for removal in removals:
            removals += remove_duplicates(removal)

    return list(set(removals))


# Binary search for dictionary lookups: use .lower() to avoid case errors 
# in searching, e.g. 'job' > 'Job', despite extra memory used by generating 
# new strings for each comparison.

def word_search(dictionary, word, start, end):
    if end - start <= 1:
        return None 
    else:
        middle = int((start + end) / 2)

        if word == dictionary[middle]:
            return dictionary[middle]

        elif word < dictionary[middle] or word < dictionary[middle].lower():
            return word_search(dictionary, word, start, middle)
        elif word > dictionary[middle] or word > dictionary[middle].lower():
            return word_search(dictionary, word, middle, end)


# From the list of suggestions generated by spellcheck(), return the first word 
# that's found in the wordlist dictionary of most common English words. (If none,
# arbitrarily return suggestions[0] instead.)

def check_frequencies(suggestions):
    for each in sorted(suggestions):
        if wordlist.get(each):
            return each
    return suggestions[0]



if __name__ == "__main__":
    main()
