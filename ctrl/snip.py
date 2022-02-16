
import logging
import random
import re

import model.snip

SLUG_REGEX = re.compile(r"^[a-zA-Z]+$")


def _isValidSlug(slug):
  return SLUG_REGEX.match(slug) != None


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

def getSnipPath(slug):
  if not _isValidSlug(slug):
    return None
  return model.snip.getSnipPath(slug)
