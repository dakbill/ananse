import json
from datetime import datetime
import os
from elasticsearch import Elasticsearch
from google.appengine.ext.webapp import template
import webapp2


es = Elasticsearch()


class Fetcher():
    def __init__(self):
        pass


class Parser():
    def __init__(self):
        pass

    @staticmethod
    def parse(url):
        es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})


class RulesHandler(webapp2.RedirectHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'create_rule.html')
        self.response.write(template.render(path, {}))
