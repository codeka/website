
from google.appengine.ext import db
from google.appengine.ext.blobstore import blobstore

class Snip(db.Model):
  """A snip is basically a blob with a bit of extra metadata."""
  slug = db.StringProperty()
  posted = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)
  blob = blobstore.BlobReferenceProperty()
  width = db.IntegerProperty()
  height = db.IntegerProperty()
