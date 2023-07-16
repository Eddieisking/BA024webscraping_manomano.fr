# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql
import re
import googletrans
from datetime import datetime, timedelta
from googletrans import Translator
from pymysql import Error


# Pipeline for Excel
class ExcelPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = 'customer reviews'
        self.ws.append(('product_name','customer_name', 'customer_rating', 'customer_date', 'customer_review', 'customer_support', 'customer_purchase_date'))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.wb.save('manomano.xlsx')

    def process_item(self, item, spider):
        # review_id = item.get('review_id', '')
        product_name = item.get('product_name', '')
        customer_name = item.get('customer_name', '')
        customer_rating = item.get('customer_rating', '')
        customer_date = item.get('customer_date', '')
        customer_review = item.get('customer_review', '')
        customer_support = item.get('customer_support', '')
        # customer_disagree = item.get('customer_disagree', '')
        customer_purchase_date = item.get('customer_purchase_date', '')

        self.ws.append((product_name, customer_name, customer_rating, customer_date, customer_review, customer_support, customer_purchase_date))
        return item


# Pipeline for sql
def remove_unappealing_characters(text):
    # Remove emojis
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E]', '', text)

    return text

def translator(text: str, src: str):

    # print(googletrans.LANGUAGES)

    translator = Translator()
    result = translator.translate(text, src=src, dest='en')

    return result.text

def extract_translate_month(date_str, src):
    translator = Translator()
    month_italian = date_str.split()[1]
    translated_month = translator.translate(month_italian, src=src, dest='en').text
    translated_date_str = date_str.replace(month_italian, translated_month)

    return translated_date_str

def convert_to_datetime(date_info):
    def date(date_str):
        date_object = datetime.strptime(date_str, '%d %B %Y')
        date = date_object.date()
        return date

    current_date = datetime.now().date()  # Get current date without time
    # if '年前' in date_info:
    #     years_ago = int(date_info.split('年前')[0])
    #     date = current_date - timedelta(days=years_ago * 365)
    if 'semaine' in date_info:
        weeks_ago = int(re.findall(r"(\d+)\s+semaine", date_info)[0])
        date = current_date - timedelta(days=weeks_ago * 7)
    elif 'jour' in date_info:
        days_ago = int(re.findall(r"(\d+)\s+jour", date_info)[0])
        date = current_date - timedelta(days=days_ago)
    else:
        date = date(extract_translate_month(date_info, src='fr'))

    return date

def extract_rating(text):
    pattern = r'(\d+)/5'
    match = re.search(pattern, text)

    if match:
        return int(match.group(1))
    else:
        return None

def find_number(text):
    # Use regular expression to find a number in the text
    pattern = r"\d+"
    match = re.search(pattern, text)

    if match:
        number = int(match.group())
        return number
    else:
        return 0

class DatabasePipeline:

    def __init__(self):
        self.conn = pymysql.connect(user="fqmm26", password="boston27", host="myeusql.dur.ac.uk", database="Pfqmm26_BA024")
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0:
            self.sql_write()
        # self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("SELECT 1")  # Execute a simple query to check if the connection is alive
        except Error as e:
            print(f"Error: {e}")
            self.reconnect()

        # review_id = item.get('review_id', '')
        review_id = 'N/A'
        product_name = item.get('product_name', '')
        customer_name = item.get('customer_name', '')
        customer_rating = extract_rating(item.get('customer_rating', ''))
        customer_date = convert_to_datetime(item.get('customer_date', ''))
        customer_review = item.get('customer_review', '')[0:1999]
        customer_support = find_number(item.get('customer_support', ''))
        # customer_disagree = item.get('customer_disagree', '')
        customer_disagree = 0
        # customer_purchase_date = item.get('customer_purchase_date', '')

        product_name_en = translator(product_name, src='fr')
        customer_review_en = translator(customer_review, src='fr')

        self.data.append((review_id, product_name, customer_name, customer_rating, customer_date, customer_review, customer_support, customer_disagree, product_name_en, customer_review_en))

        if len(self.data) == 10:
            self.sql_write()
            self.data.clear()

        return item

    def sql_write(self):
        self.cursor.executemany(
            "insert into manomano_fr (review_id, product_name, customer_name, customer_rating, customer_date, customer_review, customer_support, customer_disagree, product_name_en, customer_review_en) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            self.data
        )
        self.conn.commit()

    def reconnect(self):
        try:
            self.conn.ping(reconnect=True)  # Ping the server to reconnect
            print("Reconnected to the database.")
        except Error as e:
            print(f"Error reconnecting to the database: {e}")
