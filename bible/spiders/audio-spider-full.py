import json
import scrapy
import requests
from pathlib import Path

class AudioBibleSpider(scrapy.Spider):
    

    name = 'audio-bible-full'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

		# change the language version number the three following line
		# Iu Mien New Roman: 233 ARA: 1608
        self.bible_id = '1957-full'
        self.base_url = "https://events.bible.com/api/bible/chapter/3.1?id=1957&reference="
        self.start_urls = [
            'https://events.bible.com/api/bible/chapter/3.1?id=1957&reference=GEN.1'
        ]

    def parse(self, response):
        print("XXXXXXXXXXXXXXXXXXX")
        print(response)
        data = json.loads(response.body.decode('utf-8'))
        if data['audio'] is not None:
            mp3_url = 'https:' + data['audio'][0]['download_urls']['format_mp3_32k']

            book_name = mp3_url.split('/')[-2]
            chapter = mp3_url.split('/')[-1].split('-')[0]
            file_type = mp3_url.split('/')[-1].split('.')[-1].split('?')[0]

            path = Path(f"bible/data/{self.bible_id}/{book_name}")
            path.mkdir(parents=True, exist_ok=True)

            audio_bytes = requests.get(mp3_url).content
            with open(path / f"{self.bible_id}-{book_name}-{chapter}.{file_type}", 'w+b') as audio_file:
                audio_file.write(audio_bytes)


        next_chapter = data['next']

        if next_chapter is None:
            yield []
        else:
            yield scrapy.Request(
                self.base_url+next_chapter['usfm'][0],
                callback=self.parse
            )
