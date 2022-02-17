
from errno import ERANGE
import logging
import os
import random
import re
import tempfile

from PIL import Image
from werkzeug.utils import secure_filename

import model.snip

SLUG_REGEX = re.compile(r"^[a-zA-Z]+$")
SLUG_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif'}


def _isValidSlug(slug):
  return SLUG_REGEX.match(slug) != None


def _isAllowedUploadName(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getSnipPath(slug):
  if not _isValidSlug(slug):
    return None
  return model.snip.getSnipPath(slug)


def getSnip(slug):
  if not _isValidSlug(slug):
    return None
  return model.snip.loadSnip(slug)


def saveSnip(file):
  if not _isAllowedUploadName(file.filename):
    logging.warning("Filename not allowed: " + file.filename)
    return None

  slug = ""
  while True:
    slug = ""
    for _ in range(12):
      slug += random.choice(SLUG_CHARS)
    # TODO: check whether the slug already exists (unlikely but possible)
    break

  model.snip.saveSnipFile(file, slug)

  snip = model.snip.Snip()
  snip.slug = slug
  filename, ext = os.path.splitext(os.path.basename(secure_filename(file.filename)))
  snip.filename = filename + ext

  img = Image.open(file)
  snip.width, snip.height = img.size

  if img.format == 'JPEG' or img.format == 'JPG':
    snip.contentType = 'image/jpg'
    snip.filename = filename + '.jpg'
  elif img.format == 'PNG':
    snip.contentType = 'image/png'
    snip.filename = filename + '.png'
  elif img.format == 'GIF':
    snip.contentType = 'image/gif'
    snip.filename = filename + '.gif'
  else:
    snip.contentType = 'image/png' # TODO: unknown?

  model.snip.saveSnip(snip)
  return snip

