
import os
import datetime
import webapp2 as webapp

import ctrl.blog
import handlers


class BlogPage(handlers.BaseHandler):
  pass


class HomePage(BlogPage):
  def get(self):
    self.render('index.html', {})


class ShowcasePage(BlogPage):
  def get(self):
    self.render('showcase.html', {})


app = webapp.WSGIApplication([('/?', HomePage),
                              ('/showcase', ShowcasePage)],
                             debug=os.environ['SERVER_SOFTWARE'].startswith('Development'))
