import json
import scrapy
import m3u8
import requests
from pathlib import Path

class AudioBibleSpider(scrapy.Spider):
    

    name = 'audio-bible'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

		# change the language version number the three following line
		# Iu Mien New Roman: 233 ARA: 1608
        self.bible_id = 1957
        self.base_url = "https://events.bible.com/api/bible/chapter/3.1?id=1957&reference="
        self.start_urls = [
            'https://events.bible.com/api/bible/chapter/3.1?id=1957&reference=GEN.1'
        ]

    def parse(self, response):
        print("XXXXXXXXXXXXXXXXXXX")
        print(response)
        data = json.loads(response.body.decode('utf-8'))
        if data['audio'] is not None:
            m3u8_url = 'https:' + data['audio'][0]['download_urls']['format_hls']

            playlist = m3u8.load(m3u8_url)

            base_audio_url = m3u8_url.rsplit('/', 1)[0]
            book_name = m3u8_url.split('/')[-2]
            chapter = m3u8_url.split('/')[-1].split('-')[0]


            path = Path(f"bible/data/{self.bible_id}/{book_name}/{chapter}")
            path.mkdir(parents=True, exist_ok=True)


            for index, segment in enumerate(playlist.segments):
                segment_file_type = segment.uri.split('.')[-1]
                audio_bytes = requests.get(f'{base_audio_url}/{segment.uri}').content
                with open(path / f"{self.bible_id}-{book_name}-{chapter}-{index}.{segment_file_type}", 'w+b') as audio_file:
                    audio_file.write(audio_bytes)

        next_chapter = data['next']

        if next_chapter is None:
            yield []
        else:
            yield scrapy.Request(
                self.base_url+next_chapter['usfm'][0],
                callback=self.parse
            )
