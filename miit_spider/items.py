# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class VehicleItem(Item):
    gid = Field()
    cpid = Field()
    pc = Field()
    gppc = Field()
    cph = Field()
    qyid = Field()
    qymc = Field()
    cpsb = Field()
    clxh = Field()
    clmc = Field()
    dataTag = Field()
