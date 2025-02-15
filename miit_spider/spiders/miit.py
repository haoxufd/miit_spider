import scrapy


import scrapy
import json
from urllib.parse import quote
from ..items import VehicleItem

class MiitSpider(scrapy.Spider):
    name = 'miit'
    allowed_domains = ['app.miit-eidc.org.cn']
    
    custom_settings = {
        'FEEDS': {
            'items.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'ensure_ascii': False,
                }
            }
        }
    }

    def start_requests(self):
        url = "https://app.miit-eidc.org.cn/miitxxgk/gonggao/xxgk/doCpQuery"
        headers = {
            "Accept": "application/json, text/javascript, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://app.miit-eidc.org.cn",
            "Referer": "https://app.miit-eidc.org.cn/miitxxgk/gonggao_xxgk/index_ggcp.html",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        # 总页数
        total_pages = 3799
        
        for page in range(1, total_pages + 1):
            form_data = {
                "qymc": "",
                "pc": "",
                "cpsb": "",
                "clxh": "",
                "clmc": quote("电动"),
                "scdz": "",
                "cplb": "0",
                "cxtype": "",
                "pageSize": "10",
                "pageNum": str(page)
            }
            
            yield scrapy.FormRequest(
                url=url,
                method='POST',
                formdata=form_data,
                headers=headers,
                callback=self.parse,
                meta={'page': page},
                dont_filter=True
            )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            page = response.meta['page']
            
            self.logger.info(f"Processing page {page}")
            
            if 'cpList' in data:
                for vehicle in data['cpList']:
                    item = VehicleItem()
                    for field in item.fields:
                        item[field] = vehicle.get(field)
                    yield item
            else:
                self.logger.error(f"No cpList in response for page {page}")
                
        except json.JSONDecodeError:
            self.logger.error(f"JSON decode error on page {page}")
        except Exception as e:
            self.logger.error(f"Error processing page {page}: {str(e)}")
