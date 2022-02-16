import datetime
import os
import yaml

from flask import current_app


class Snip(yaml.YAMLObject):
  """A snip is a file we store locally with a bit of extra metadata."""
  def __init__(self, slug="", posted=datetime.datetime.now(), updated=datetime.datetime.now(),
               width=0, height=0, contentType="image/png"):
    self.slug = slug
    self.posted = posted
    self.updated = updated
    self.width = width
    self.height = height
    self.contentType = contentType


def _rootPath():
  return os.path.join(current_app.config['DATA_PATH'], 'snips')


def getSnipPath(slug):
  return os.path.join(_rootPath(), slug[0:2] + '/' + slug[2:] + '.dat')
