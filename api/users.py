import json
from py2neo import Graph
from pymongo import MongoClient
import webapp2

remote_graph = Graph(
    'http://xcite_graph_db:uJg6WvK3AFjzRukDKZWd@xcitegraphdb.sb02.stations.graphenedb.com:24789/db/data/'
)

client = MongoClient()
db = client['ananse']

User = db['user']


class UsersHandler(webapp2.Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        mobile_numbers = [record.mobileNumber for record in
                          remote_graph.cypher.execute('match (u:User) return u.mobileNumber as mobileNumber')]
        self.response.write(json.dumps({
            'message': 'success',
            'results': mobile_numbers
        }))
