BOT_NAME = 'bible'

SPIDER_MODULES = ['bible.spiders.spider', 'bible.spiders.audio-spider', 'bible.spiders.audio-spider-full', 'bible.spiders.audio-spider-full-name']
NEWSPIDER_MODULE = 'bible.spiders'

LOG_ENABLED = True

ITEM_PIPELINES = {
    'bible.pipelines.BiblePipeline': 300,
}
