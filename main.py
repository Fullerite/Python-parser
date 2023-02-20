import json
import requests
from bs4 import BeautifulSoup


def parse_words(url: str) -> tuple:
    """Creating request, parsing russian words and english definitions"""

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    ru_words_latin_1 = soup.find_all('td', {'class': 'word'})  # parsing <td> with ru words(they're in Latin-1 encoding)

    ru_words = []
    en_words = []
    for word in ru_words_latin_1:
        ru_words.append(word.get_text().encode('iso-8859-1').decode('utf-8', errors='ignore'))  # Latin-1 to UTF-8
        en_words.append(word.find_next_sibling().get_text())  # en words are in the next <td> after <td> with ru words

    return ru_words, en_words


def save_parsed_data(url: str) -> None:
    """Saving parsed data into JSON file"""

    words_dict = {}

    for page_number in range(1, 12 + 1):
        if page_number == 1:  # the first page is just most_common_words
            ru_words, en_words = parse_words(url)
            ru_words = list(map(lambda word: word.strip(), ru_words))
            en_words = list(map(lambda word: word.strip(), en_words))
            for ru, en in zip(ru_words, en_words):
                words_dict[ru] = en
        else:  # other pages are most_common_words_{number}
            url = f'http://masterrussian.com/vocabulary/most_common_words_{page_number}.htm'
            ru_words, en_words = parse_words(url)
            ru_words = list(map(lambda word: word.strip(), ru_words))
            en_words = list(map(lambda word: word.strip(), en_words))
            for ru, en in zip(ru_words, en_words):
                words_dict[ru] = en

    with open('words.json', 'w') as file:
        json_obj = json.dumps(words_dict, indent=4)
        file.write(json_obj)


if __name__ == '__main__':
    url = 'http://masterrussian.com/vocabulary/most_common_words.htm'
    save_parsed_data(url)
