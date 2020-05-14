import json
import scrapy

class BibleSpider(scrapy.Spider):
    

    name = 'bible'

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
        text = data['content']

        html = scrapy.http.HtmlResponse(
            response.url,
            body=text,
            encoding='utf-8'
        )

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

        if 'INTRO' not in chapter:
            if book not in verses:
                verses[book] = {}

            if chapter not in verses[book]:
                verses[book][chapter] = {}
                
            number = 0
            chapter_div = html.css(".chapter")[0]
            for container in chapter_div.css('div'):
                heading = container.css(".heading::text")
                if heading:
                    if chapter_div.attrib['class'] != container.attrib['class']:
                        # Using ahlf verse number for heading
                        verses[book][chapter][f'{number}.5'] = heading.extract()
                    continue

                if container.css(".verse"):
                    for verse in container.css(".verse"):
                        number = verse.css(".verse").xpath('@data-usfm').extract_first().split(".")[-1]
                        text = verse.css('.content::text').extract()
                        if number not in verses[book][chapter]:
                            verses[book][chapter][number] = ''

                        text.extend([' ']) # adding space after the end of the sentence
                        texto = ''.join(text)
                        if len(texto.strip()) > 0:
                            # excluding texts that only contains spaces
                            verses[book][chapter][number] += texto

        if next_chapter is None:
        # if int(chapter) > 3:
            yield verses
        else:
            yield scrapy.Request(
                self.base_url+next_chapter,
                callback=self.parse,
                meta={'verses': verses}
            )
