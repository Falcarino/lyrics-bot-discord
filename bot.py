import discord
import asyncio
from lyrics_parser import Song


class LyricsBot(discord.Client):
    available_languages = {'English': '🇨🇦',
                           'Japanese': '🇧🇩',
                           'Korean': '🇰🇵',
                           'Chinese': '🇹🇼',
                           'Portuguese': '🇦🇴'}
    msg_links = dict()

    def __init__(self):
        intents = discord.Intents(message_content=True, messages=True, reactions=True, guilds=True)
        super().__init__(intents=intents)
        self.channel = None

    async def on_ready(self):
        self.channel = self.get_channel(897376538805272618)
        print(f'Logged in as {self.user}. I operate only in #{self.channel}')

    async def remove_reference(self, msg_id, delay=5):
        await asyncio.sleep(delay)
        self.msg_links.pop(msg_id)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$check'):
            await self.channel.send(f':flag_am:\n{message.created_at.strftime("%H:%M:%S")}', delete_after=5)

        if message.content.startswith('$lyrics'):
            msg_lifespan = 40
            song = Song()
            msg = await self.channel.send(song.get_lyrics(), delete_after=msg_lifespan)

            if song.languages is not None:
                for language in song.languages:
                    await msg.add_reaction(self.available_languages.get(language, '😵‍💫'))

                self.msg_links[msg.id] = {'lyrics_msg': None, 'song': song}
                for k, v in self.msg_links.items():
                    print(v['song'].name)
                await self.remove_reference(msg.id, delay=msg_lifespan)

    async def on_raw_reaction_add(self, payload):
        user_id = payload.user_id
        msg_id = payload.message_id
        if self.get_user(user_id) == self.user:
            return
        if msg_id not in self.msg_links:
            return

        msg_link = self.msg_links[msg_id]
        language = next(l for l, l_code in self.available_languages.items() if l_code == payload.emoji.name)
        if msg_link['lyrics_msg'] is None:
            msg = await self.channel.send(msg_link['song'].print_lyrics(language))
            msg_link['lyrics_msg'] = msg
        else:
            new_lyrics = msg_link['song'].print_lyrics(language)
            await msg_link['lyrics_msg'].edit(content=f'{new_lyrics}')


