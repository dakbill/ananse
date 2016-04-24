import json
from elasticsearch import Elasticsearch
import webapp2

es = Elasticsearch()


class ItemsHandler(webapp2.RedirectHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        print es.get(index="my-index", doc_type="test-type", id=42)['_source']
        self.response.write(json.dumps({
            'message': 'success',
            'results': [
                {
                    'title': 'title',
                    'description': 'description',
                    'type': 'blog',
                    'url': 'https://httpbin.org/get',
                    'image': 'https://placehold.it/100x100'
                },
                {
                    'title': 'title',
                    'description': 'description',
                    'type': 'blog',
                    'url': 'https://httpbin.org/get',
                    'image': 'https://placehold.it/100x100'
                },
                {
                    'title': 'title',
                    'description': 'description',
                    'type': 'blog',
                    'url': 'https://httpbin.org/get',
                    'image': 'https://placehold.it/100x100'
                }
            ]
        }))