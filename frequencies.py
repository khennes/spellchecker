# This program makes a request to the Wiktionary API for the contents of its 
# page with the top 10,000 most common English words. It then uses Beautiful Soup 
# to scrape the HTML and extract the contents of each <a> tag (which contain the 
# actual words) to the Python list WORDS. Finally, it adds each word in WORDS 
# as a key to a dictionary whose value is equal to its index in WORDS (to 
# preserve the order of the original list), and writes the dict to a JSON file.


import urllib2
from bs4 import BeautifulSoup
import json


def make_wordlist():

    # Retrieve the contents of the Wikitionary page and store as an HTML string
    text_file = urllib2.urlopen('http://en.wiktionary.org/w/api.php?action=parse&format=txt&pageid=267872&prop=text&contentformat=text%2Fplain&contentmodel=text').read()

    soup = BeautifulSoup(text_file)  # create a Beautiful Soup object

    WORDS = []
    wordlist = {}

    all_words = soup.find_all('a')  # scrape the Soup object for <a> tags

    for each in all_words:
        word = str(''.join(each.contents))  # extract text node from each <a> tag
        WORDS.append(word)

    for word in WORDS:
        wordlist[word] = WORDS.index(word)

    f = open('wordlist.json', 'w+')
    json.dump(wordlist, f)
    f.close()


if __name__ == "__main__":
    make_wordlist()
