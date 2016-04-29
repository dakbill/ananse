from elasticsearch import Elasticsearch
from pymongo import MongoClient

import json
import webapp2


es = Elasticsearch()
client = MongoClient()
db = client['ananse']

Item = db['item']


class ItemsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        # print es.get(index="my-index", doc_type="test-type", id=42)['_source']
        self.response.write(json.dumps({
            'results':list(Item.find({}, {'_id': 0})),
            'message':'Success'
        }))