from scrapy.commands import BaseRunSpiderCommand
from scrapy.exceptions import UsageError


class Command(BaseRunSpiderCommand):
    requires_project = True

    def syntax(self):
        return "[options] [<spider> ...]"

    def short_desc(self):
        return "Run multiple spiders"

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()

        for spider_name in args:
            spider_cls = self.crawler_process.spider_loader.load(spider_name)
            self.crawler_process.crawl(spider_cls)
        self.crawler_process.start()
