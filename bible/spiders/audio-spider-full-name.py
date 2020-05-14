import json
import scrapy
import requests
from pathlib import Path

class AudioBibleSpider(scrapy.Spider):
    

    name = 'audio-bible-full-name'

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
        mp3_url = None
        if data['audio'] is not None:
            mp3_url = 'https:' + data['audio'][0]['download_urls']['format_mp3_32k']


        text = data['content']

        if 'verses' not in response.meta:
            verses = {}
        else:
            verses = response.meta['verses']


        book = data['reference']['human'].split(" ")
        book.pop(-1)
        book = " ".join(book)
        chapter = data['reference']['usfm'][0].split(".")[1]

        next_chapter = data['next']
        if next_chapter is not None:
            next_chapter = next_chapter['usfm'][0]

        if book not in verses:
            verses[book] = {}

        if chapter not in verses[book]:
            verses[book][chapter] = {}

        verses[book][chapter]['mp3'] = mp3_url
            

        if next_chapter is None:
            yield verses
        else:
            yield scrapy.Request(
                self.base_url+next_chapter,
                callback=self.parse,
                meta={'verses': verses}
            )
