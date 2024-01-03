import json
import re
import time
from get_chrome_driver import GetChromeDriver
from selenium import webdriver

import requests
from bs4 import BeautifulSoup
from get_chrome_driver import GetChromeDriver

from naverplaceapi.mixin.utils import HEADERS, parse_naver_var_in_script_texts
from . import query


class ReviewMixin:
    def get_visitor_reviews(self, business_id: str, page_no: int, page_cnt: int, proxies=None):
        data = query.get_visitor_reviews.create(business_id, page_no, page_cnt)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['visitorReviews']
        if graphql_data is None:
            graphql_data = {}
        # ['visitorReviews']
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_ugc_reviews(self, business_id: str, page_no: int, page_cnt: int, proxies=None):
        data = query.get_ugc_reviews.create(business_id, page_no, page_cnt)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['restaurant']['fsasReviews']
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_visitor_review_stats(self, business_id: str, proxies=None):
        data = query.get_visitor_review_stats.create(business_id)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['visitorReviewStats']
        if graphql_data is None:
            return None
        graphql_data['_id'] = graphql_data['id']
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_visitor_review_photos_in_visitor_review_tab(self, store_id: str, page_no: int, page_size: int,
                                                        proxies=None):
        data = query.get_visitor_review_photos_in_visitor_review_tab.create(store_id, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['visitorReviews']
        if graphql_data is None:
            graphql_data = {}
        graphql_data['business_id'] = store_id
        return graphql_data

    def get_visitor_review_theme_lists(self, store_id: str, page_no, page_size, proxies=None):
        data = query.get_visitor_review_theme_lists.create(store_id, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['themeLists']
        graphql_data['business_id'] = store_id

        return graphql_data

    def get_blog_reviews_in_html(self, business_id: str, proxies=None):
        get_driver = GetChromeDriver()
        get_driver.install()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome(options=options)
        url = "https://pcmap.place.naver.com/restaurant/{}/review/ugc?type=photoView".format(business_id)
        driver.get(url)
        html_text = driver.page_source


        # url = "https://pcmap.place.naver.com/restaurant/{}/review/ugc?type=photoView".format(business_id)
        # response = requests.get(url, proxies=proxies)
        # response.raise_for_status()
        # html_text = response.content

        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")

        naver_var = parse_naver_var_in_script_texts(scripts)
        variable_name = 'window.__APOLLO_STATE__'
        pattern = re.compile(rf'\b{re.escape(variable_name)}\s*=\s*(.*?)(\n)')
        match = pattern.search(naver_var)

        if match:
            data = match.group(1)
            return json.loads(data[:-1])
        else:
            return None

    def get_visitor_reviews_in_html(self, business_id: str, proxies=None):
        get_driver = GetChromeDriver()
        get_driver.install()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome(options=options)
        url = "https://pcmap.place.naver.com/restaurant/{}/review/visitor".format(business_id)
        driver.get(url)
        html_text = driver.page_source


        # url = "https://pcmap.place.naver.com/restaurant/{}/review/visitor".format(business_id)
        # response = requests.get(url, proxies=proxies)
        # response.raise_for_status()
        # html_text = response.content

        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")

        naver_var = parse_naver_var_in_script_texts(scripts)
        variable_name = 'window.__APOLLO_STATE__'
        pattern = re.compile(rf'\b{re.escape(variable_name)}\s*=\s*(.*?)(\n)')
        match = pattern.search(naver_var)

        if match:
            data = match.group(1)
            return json.loads(data[:-1])
        else:
            return None
