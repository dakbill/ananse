#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import sys
from api.items import ItemsHandler
from api.spider import RulesHandler
from api.users import UsersHandler

sys.path.insert(0, 'libs')

from google.appengine.ext.webapp import template
from py2neo import Graph
from elasticsearch import Elasticsearch

import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        self.response.write(template.render(path, {}))


app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/items', ItemsHandler),
                                  ('/rules', RulesHandler),
                                  ('/users', UsersHandler),
                              ], debug=True)
