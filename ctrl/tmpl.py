import datetime
import json
import os
from flask import current_app, request

from . import ctrl


@ctrl.app_template_filter()
def post_tags(post):
  return ', '.join(post.tags)


@ctrl.app_template_filter()
def post_url(post):
  return '%04d/%02d/%s' % (post.posted.year, post.posted.month, post.slug)


@ctrl.app_template_filter()
def post_full_url(post):
  host = current_app.config['SERVER_NAME']
  if not host:
    host = '??'
  return '//'+host+'/blog/'+post_url(post)


@ctrl.app_template_filter()
def post_date(post):
  return post.posted.strftime('%d %b %Y')


@ctrl.app_template_filter()
def post_date_time(post):
  return post.posted.strftime('%d %b %Y %H:%M')


@ctrl.app_template_filter()
def post_date_rss(post):
  return post.posted.strftime('%a, %d %b %Y %H:%M:%S GMT')


@ctrl.app_template_filter()
def post_date_std(post):
  return post.posted.strftime('%Y-%m-%d %H:%M:%S')


@ctrl.app_template_filter()
def post_date_editable(post):
  return post.posted.strftime('%y-%m-%d %H:%M')


@ctrl.app_template_filter()
def post_extract(post):
  return post.html[0:500]+'...'


@ctrl.app_template_filter()
def dump_json(obj):
  return json.dumps(obj)


@ctrl.app_template_filter()
def number(n):
  return "{:,}".format(n)


def inject_defaults():
  return dict(
    year=datetime.datetime.now().year,
    host_server=request.server,
    url=request.url)
ctrl.app_context_processor(inject_defaults)

#  if user:
#    data['is_logged_in'] = True
#    data['logout_url'] = users.create_logout_url(self.request.uri)
#    data['is_writer'] = (user.email() == 'dean@codeka.com.au')
#    data['user'] = user
#  else:
#  data['is_logged_in'] = False
#  data['login_url'] = 'http://www.example.com'#users.create_login_url(self.request.uri)
#

#  if tmpl[-4:] == ".txt":
#    self.response.content_type = "text/plain"
#  elif tmpl[-4:] == ".rss":
#    self.response.content_type = "application/rss+xml"
#  else:
#    self.response.content_type = "text/html"
