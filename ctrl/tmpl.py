
import jinja2
import logging
import os
import re


jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/../tmpl'))


def _filter_post_id(post):
  return post.key().id()
jinja.filters['post_id'] = _filter_post_id


def _filter_post_tags(post):
  return ', '.join(post.tags)
jinja.filters['post_tags'] = _filter_post_tags


def _filter_post_url(post):
  return '%04d/%02d/%s' % (post.posted.year, post.posted.month, post.slug)
jinja.filters['post_url'] = _filter_post_url


def _filter_post_full_url(post):
  return '//'+os.environ.get('HTTP_HOST')+'/blog/'+_filter_post_url(post)
jinja.filters['post_full_url'] = _filter_post_full_url


def _filter_post_date(post):
  return post.posted.strftime('%d %b %Y')
jinja.filters['post_date'] = _filter_post_date


def _filter_post_date_time(post):
  return post.posted.strftime('%d %b %Y %H:%M')
jinja.filters['post_date_time'] = _filter_post_date_time


def _filter_post_date_rss(post):
  return post.posted.strftime('%a, %d %b %Y %H:%M:%S GMT')
jinja.filters['post_date_rss'] = _filter_post_date_rss


def _filter_post_date_std(post):
  return post.posted.strftime('%Y-%m-%d %H:%M:%S')
jinja.filters['post_date_std'] = _filter_post_date_std

def _filter_post_date_editable(post):
  return post.posted.strftime('%y-%m-%d %H:%M')
jinja.filters['post_date_editable'] = _filter_post_date_editable


def _filter_post_extract(post):
  return post.html[0:500]+'...'
jinja.filters['post_extract'] = _filter_post_extract


def _filter_dump_json(obj):
  return json.dumps(obj)
jinja.filters['dump_json'] = _filter_dump_json


def _filter_number(n):
  return "{:,}".format(n)
jinja.filters["number"] = _filter_number


def getTemplate(tmpl_name):
  return jinja.get_template(tmpl_name)


def render(tmpl, data):
  return tmpl.render(data)
