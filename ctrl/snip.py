
import logging
import random

from google.appengine.api import images
from google.appengine.api import memcache

import model.snip

def createSnip(blobKey):
  slug = ""
  while True:
    slug = ""
    for _ in xrange(12):
      slug += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # TODO: check whether the slug already exists (unlikely but possible)
    break

  img = images.Image(blob_key=blobKey)
  img.im_feeling_lucky() # we have to do a transform in order to get dimensions
  img.execute_transforms()

  snip = model.snip.Snip()
  snip.slug = slug
  snip.blob = blobKey
  snip.width = img.width
  snip.height = img.height
  snip.put()

  memcache.set('snip:%s' % slug, snip)

  return snip

def getSnip(slug):
  keyname = 'snip:%s' % slug
  snip = memcache.get(keyname)
  if not snip:
    for snip in model.snip.Snip.all().filter('slug', slug):
      memcache.set(keyname, snip)
      return snip
  return snip
