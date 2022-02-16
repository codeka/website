
import logging
import random
import re

import model.snip

SLUG_REGEX = re.compile(r"^[a-zA-Z]+$")


def _isValidSlug(slug):
  return SLUG_REGEX.match(slug) != None


def getSnipPath(slug):
  if not _isValidSlug(slug):
    return None
  return model.snip.getSnipPath(slug)
