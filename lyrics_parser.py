import requests
from bs4 import BeautifulSoup
import random

MAX_QUERY_RESULT = 1000 # if you set the "limit" parameter in the query over 1000, it will only give you 1000
PAGINATION_LIMIT = 5


class Song:
    characters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]

    def __init__(self):
        self.languages = None
        self.name = None
        self.all_lyrics = None

    @staticmethod
    def get_random_song():
        first_character = random.choice(Song.characters)
        page = random.randint(1, MAX_QUERY_RESULT // PAGINATION_LIMIT)
        # TODO: redo the dice roll since sometimes number of found songs is less than the pagination limit
        # scrap the whole dice thing, get the songs list from the search page and do random.choice()
        dice_roll = random.randint(0, PAGINATION_LIMIT - 1)

        url = f'https://vocaloidlyrics.fandom.com/wiki/Special:Search?scope=internal&query={first_character}&lang=en&limit={PAGINATION_LIMIT}&page={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        song_list = soup.find('ul', {'class': 'unified-search__results'})
        song = song_list.find_all('li', {'class': 'unified-search__result'})[dice_roll]
        song_url = song.find('a')['href']
        return song_url

    def get_lyrics(self):
        url = Song.get_random_song()
        print(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        name = soup.find('h1', {'id': 'firstHeading'})
        if name is not None:
            self.name = name.get_text(strip=True)

        lyrics_header = soup.select_one('h2', text='Lyrics')
        self.all_lyrics = lyrics_header.find_next_sibling('table')
        if self.all_lyrics is None:
            return f'Couldn\'t find the lyrics table for **"{self.name}"**'
        languages_tr = self.all_lyrics.find('tr')

        self.languages = [language.get_text(strip=True) for language in languages_tr.find_all('td')]
        self.all_lyrics = self.all_lyrics.find_all('tr')[1:]

        return f'Found **"{self.name}"**. In what language do you want the lyrics?'

    def print_lyrics(self, language):
        lyrics = [f'**Lyrics for "{self.name}":**\n']
        language_index = self.languages.index(language)
        for row in self.all_lyrics:
            td_list = row.find_all('td')
            if len(td_list) > 1:
                lyrics.append(td_list[language_index].text)
            else:
                lyrics.append('\n')

        return ''.join(lyrics)
