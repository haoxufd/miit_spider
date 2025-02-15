# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import json
import csv
from itemadapter import ItemAdapter
from datetime import datetime

class JsonPipeline:
    def open_spider(self, spider):
        self.file = open(f'miit_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        self.first_item = False
        
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
        self.file.write(line)
        return item

class CsvPipeline:
    def open_spider(self, spider):
        self.file = open(f'miit_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', 'w', encoding='utf-8', newline='')
        self.writer = None

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        if self.writer is None:
            self.writer = csv.DictWriter(self.file, fieldnames=data.keys())
            self.writer.writeheader()
        self.writer.writerow(data)
        return item
