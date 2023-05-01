from lyrics_parser import Song
from bot import LyricsBot

with open('.token') as f:
    token = f.readline()

bot = LyricsBot()
bot.run(token)

# good_url = 'https://vocaloidlyrics.fandom.com/wiki/%E3%83%A9%E3%83%B3%E3%83%89_(Land)'
# no_table_sibling_and_no_japanese_url = 'https://vocaloidlyrics.fandom.com/wiki/Obligatory_Crow_Song'
# no_japanese_url = 'https://vocaloidlyrics.fandom.com/wiki/La_Plena_de_los_Desamores'
# print(Song.get_lyrics(no_japanese_url))
