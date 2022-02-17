import datetime
import logging
import os
import yaml

from flask import current_app
from shutil import copyfileobj


class Snip(yaml.YAMLObject):
  """A snip is a file we store locally with a bit of extra metadata."""
  def __init__(self, slug="", posted=datetime.datetime.now(), updated=datetime.datetime.now(),
               width=0, height=0, contentType="image/png", filename=""):
    self.slug = slug
    self.posted = posted
    self.updated = updated
    self.width = width
    self.height = height
    self.contentType = contentType
    self.filename = filename


def _rootPath():
  return os.path.join(current_app.config['DATA_PATH'], 'snips')


def getSnipPath(slug, ext='dat'):
  return os.path.join(_rootPath(), slug[0:2] + '/' + slug[2:] + '.' + ext)


def loadSnip(slug):
  with open(getSnipPath(slug, ext='yaml'), 'r') as f:
    return yaml.load(f, Loader=yaml.Loader)


def saveSnipFile(file, slug):
  path = getSnipPath(slug)
  if not os.path.isdir(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))
  with open(getSnipPath(slug), "wb") as f:
    copyfileobj(file, f)


def saveSnip(snip):
  path = getSnipPath(snip.slug)
  with open(getSnipPath(snip.slug, ext='yaml'), "w") as f:
    yaml.dump(snip, f)
