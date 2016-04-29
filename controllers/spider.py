import json
from urlparse import urljoin
from string import ascii_lowercase
import os

from bs4 import BeautifulSoup
from threading import Thread

from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import webapp2


es = Elasticsearch()
client = MongoClient()
db = client['ananse']

SiteRule = db['site_rule']
Item = db['item']


def fetch_urls():
    return ['https://www.hellofood.com.gh/restaurants?gclid=CITktezqr8wCFcG6GwodG24OXQ']


def classify(title, description):
    text = title + description
    alphabet_count = {}
    for letter in ascii_lowercase:
        alphabet_count[letter] = ((text.count(letter) * 1.0) / text.__len__()) * 100 if letter in text else 0
    print 'Features'
    print '----------------------------------------------------------------'
    print ''.join(['%02d' % alphabet_count[key] for key in alphabet_count])


def parse():
    urls = fetch_urls()
    for url in urls:
        site_rule = SiteRule.find_one()
        content = urlfetch.fetch(url).content
        soup = BeautifulSoup(content, 'html.parser')
        for item in soup.select(site_rule.get('itemsSelector')):
            try:
                title = ' '.join(
                    [str(element.get_text()).strip() for element in item.select(site_rule.get('titleSelector'))])
                description = ' '.join([str(element.get_text()).strip() for element in
                                        item.select(site_rule.get('descriptionSelector'))])
                classify(title, description)
                Item.update({
                                'url': [urljoin(url, str(element['href']).strip()) for element in
                                        item.select(site_rule.get('urlSelector'))][0]
                            },
                            {
                                "title": title,
                                "description": description,
                                "type": "blog",
                                "image": [str(element['src']).strip() for element in
                                          item.select(site_rule.get('imageSelector'))][0],
                                "url": [urljoin(url, str(element['href']).strip()) for element in
                                        item.select(site_rule.get('urlSelector'))][0]
                            }, upsert=True)
            except Exception as ex:
                print ex

                # print item.select(site_rule.get('descriptionSelector'))
                # es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})


class RulesHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'create_rule.html')
        self.response.write(template.render(path, {}))


class IndexesHandler(webapp2.RequestHandler):
    def get(self):
        parse()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'message': 'success',
            'results': {}
        }))