
import os
import datetime
import webapp2 as webapp

import ctrl.blog
import handlers


class BasePage(handlers.BaseHandler):
  pass


class HomePage(BasePage):
  def get(self):
    self.render('index.html', {})


class ShowcasePage(BasePage):
  def get(self):
    self.render('showcase.html', {})


class NotFoundPage(BasePage):
  def get(self):
    self.error(404)


app = webapp.WSGIApplication([('/?', HomePage),
                              ('/showcase', ShowcasePage),
                              ('.*', NotFoundPage)],
                             debug=os.environ['SERVER_SOFTWARE'].startswith('Development'))
