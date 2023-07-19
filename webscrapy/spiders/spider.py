"""
Project: Web scraping for customer reviews
Author: Hào Cui
Date: 07/04/2023
"""
import time

from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC

import scrapy
from scrapy import Request
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils import create_chrome_driver
from webscrapy.items import WebscrapyItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["www.manomano.fr", "api.bazaarvoice.com", "iam.manomano.fr", "taobao.com"]
    headers = {}  #

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.browser = None

    def start_requests(self):
        # keywords = ['Stanley', 'Black+Decker', 'Craftsman', 'Porter-Cable', 'Bostitch', 'Facom', 'MAC Tools', 'Vidmar', 'Lista', 'Irwin Tools', 'Lenox', 'Proto', 'CribMaster', 'Powers Fasteners', 'cub-cadet', 'hustler', 'troy-bilt', 'rover', 'BigDog Mower', 'MTD']
        # exist_keywords = ['dewalt', 'Stanley', 'Black+Decker', 'Craftsman', 'Porter-Cable', 'Bostitch', 'Facom', 'MAC Tools', 'Vidmar', 'Lista', 'Irwin Tools', 'Lenox', 'Proto', 'CribMaster', 'Powers Fasteners', 'cub-cadet', 'hustler', 'troy-bilt', 'rover', 'BigDog Mower', 'MTD']

        """This part should be changed by finding the page numbers of different brand"""
        for page in range(3):
            start_url = f'https://www.manomano.fr/marque/black-decker-6514?page={page}'
            # 'https://www.manomano.fr/marque/dewalt-3?page=4'
            # 'https://www.manomano.fr/marque/stanley-26?page=9'
            # 'https://www.manomano.fr/marque/irwin-7?page=4'
            # 'https://www.manomano.fr/marque/bostitch-27?page=5'
            # 'https://www.manomano.fr/marque/facom-651?page=40'
            # 'https://www.manomano.fr/marque/black-decker-6514?page=3'
            

            # Load start_url
            self.browser = create_chrome_driver(headless=False)
            self.browser.get(start_url)

            time.sleep(5)
            product_links = self.browser.find_elements(By.XPATH,
                                                 '//div[@class="tG5dru c5PGVKq"]/a')

            # Print the extracted information
            review_url_list = []
            for i in range(0, len(product_links)):
                product_url = product_links[i].get_attribute("href")
                review_url = product_url + f'#tab-reviews'
                review_url_list.append(review_url)

            """the review_url_list number can be adjusted by purpose"""
            for review_url in review_url_list:
                self.browser = create_chrome_driver(headless=False)
                self.browser.get(review_url)
                """Click the custom infor"""
                self.browser.find_element(By.XPATH, '//button[@id="didomi-notice-agree-button"]').click()

                time.sleep(5)
                try:
                    self.browser.find_element(By.XPATH, '//input[@type="checkbox"]').click()
                except:
                    print('No more robot test')

                """Click the more reviews button to load all infor"""
                while True:
                    try:
                    # Click the load more button
                        more_review_button = self.browser.find_element(By.XPATH, '//div[@data-testid="see-more-reviews"]')
                        more_review_button.click()
                        time.sleep(1)
                    except:
                        print('No more pages')

                    # Click the next load more button
                    try:
                        more_review_button_new = WebDriverWait(self.browser, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="see-more-reviews"]'))
                        )
                        more_review_button = more_review_button_new
                    except:
                        print('No more extra pages')
                        break
                print('No more extra customer reviews')

                # Use selenium page source to pass the response
                body = self.browser.page_source

                """Randomly select one open website"""
                url = 'https://taobao.com/'
                # 'https://www.amazon.co.uk/'
                response = HtmlResponse(url=url, body=body, encoding='utf-8')
                # Create a new Request object based on the HtmlResponse
                request = Request(url=url, meta={'response': response}, callback=self.customer_review_parse,
                                  dont_filter=True)

                yield request

    def customer_review_parse(self, response):
        html_response = response.meta['response']
        selector = Selector(response=html_response)

        review_list = selector.xpath('//div[@class="c44RvHG"]/div[@class="jPgt-8"]')

        # Apply selectors to extract information
        for review in review_list:
            item = WebscrapyItem()

            item['product_name'] = selector.xpath('//div[@class="Z5H6D3"]/text()')[0].extract() or 'N/A'
            item['customer_name'] = review.xpath('./header/div[1]/text()')[0].extract() or 'N/A'
            item['customer_date'] = review.xpath('./header/div[2]/text()')[0].extract() or 'N/A'
            item['customer_review'] = review.xpath('.//div[@class="duBtRc c1sdlQn"]/text()')[0].extract() or 'N/A'
            item['customer_support'] = review.xpath('.//div[@class="b38yzx jKP2zg c35g1Kh gS1w88 UKD0Oa"]/text()')[
                                           0].extract() or 'N/A'

            """Some reviews have special format"""
            try:
                item['customer_rating'] = review.xpath('./div[1]/span/@aria-label')[0].extract()
                item['customer_purchase_date'] = review.xpath('./div[2]/text()')[0].extract() or 'N/A'

            except:
                item['customer_rating'] = review.xpath('./div[2]/span/@aria-label')[0].extract() or 'N/A'
                item['customer_purchase_date'] = review.xpath('./div[3]/text()')[0].extract() or 'N/A'

            yield item

