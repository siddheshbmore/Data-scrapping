import csv
import os
import random
from urllib.parse import urljoin

import requests
from lxml import html

def make_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{:02d}.0.{:04d}.{} Safari/537.36'.format(
            random.randint(63, 84), random.randint(0, 9999), random.randint(98, 132)),
    }
    return headers


timeout = 100
conn_limit = 5


class MainScraper():
    def __init__(self):
        self.result_dir = os.path.join(os.getcwd(), "Result")
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

        self.result_fname = os.path.join(self.result_dir, "Result.csv")
        self.create_result_file()

        heading = [
            "job type", "job title", "text", "html"
        ]
        if os.path.getsize(self.result_fname) == 0:
            self.insert_row(result_row=heading)

        self.total_cnt = 0
        self.total_result = []
        self.total_links = []

        self.start_urls = [
            'https://www.indeed.com/jobs?q=data+scientist&start={}',
            'https://www.indeed.com/jobs?q=software+engineer&start={}'
        ]

        self.pxy = ''
        self.sess = requests.Session()

    def start_requests(self):
        for i, url_p in enumerate(self.start_urls):
            if i == 0:
                data_type = 'Data Scientist'
            elif i == 1:
                data_type = 'Software Engineer'

            for idx in range(500):
                url = url_p.format(idx * 10)
                self.get_links(url, idx, data_type)

    def get_links(self, url, idx, data_type):
        r = self.sess.get(url=url, headers=make_headers())
        tree = html.fromstring(r.text)
        rows = tree.xpath('//h2[@class="title"]')

        for i, row in enumerate(rows):
            link = urljoin('https://www.indeed.com', row.xpath('./a/@href')[0])
            title = ''.join(row.xpath('./a//text()')).strip()
            self.get_details(link, title, data_type)

    def get_details(self, link, title, data_type):
        r = self.sess.get(link, headers=make_headers())
        tree = html.fromstring(r.text)

        save_dir = os.path.join(self.result_dir, data_type)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        text = ''.join(tree.xpath('//div[@id="jobDescriptionText"]//text()'))
        job_description_html = tree.xpath('//div[@id="jobDescriptionText"]')[0]

        # id = parse_qs(urlparse(link).query)['jk'][0]

        result_row = [
            data_type, title, text, job_description_html, r.url
        ]
        self.total_cnt += 1
        self.insert_row(result_row)
        print(f'[Total Result {self.total_cnt}] {result_row}')


    def create_result_file(self):
        self.result_fp = open(self.result_fname, 'w', encoding='utf-8-sig', newline='')
        self.result_writer = csv.writer(self.result_fp)

    def insert_row(self, result_row):
        result_row = [str(elm) for elm in result_row]
        self.result_writer.writerow(result_row)
        self.result_fp.flush()

    def spider_closed(self, spider):
        pass


if __name__ == '__main__':
    app = MainScraper()
    app.start_requests()
