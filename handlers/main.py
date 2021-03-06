
import os
import datetime
import logging
import webapp2 as webapp

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.api import users
from datetime import datetime, timedelta
import json

import ctrl.blog
import ctrl.snip
import handlers
import model.blog


class BasePage(handlers.BaseHandler):
  pass


class HomePage(BasePage):
  def get(self):
    self.render('index.html', {})


class BlobUploadUrlPage(handlers.BaseHandler):
  def get(self):
    """Gets a new upload URL for uploading blobs."""
    url = blobstore.create_upload_url('/blob/upload-complete')
    data = {'upload_url': url}
    self.response.headers['Content-Type'] = 'application/json'
    self.response.headers['Access-Control-Allow-Origin'] = '*' # TODO: restrict.
    self.response.write(json.dumps(data))


class BlobUploadCompletePage(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    blob_info = self.get_uploads('file')[0]
    response = {'success': True,
                'blob_key': str(blob_info.key()),
                'size': blob_info.size,
                'filename': blob_info.filename}
    if "X-Blob" in self.request.headers:
      response['content_type'] = blob_info.content_type
      response['url'] = '/blob/' + str(blob_info.key())
    else:
      img = images.Image(blob_key=blob_info)
      img.im_feeling_lucky() # we have to do a transform in order to get dimensions
      img.execute_transforms()
      response['width'] = img.width
      response['height'] = img.height
      response['url'] = images.get_serving_url(blob_info.key(), 100, 0)
    self.response.headers["Content-Type"] = "application/json"
    self.response.headers['Access-Control-Allow-Origin'] = '*' # TODO: restrict
    self.response.write(json.dumps(response))


class BlobPage(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, blob_key):
    blob_info = blobstore.get(blob_key)
    if not blob_info:
      self.error(404)
    else:
      self.response.headers['Cache-Control'] = 'public, max-age='+str(30*24*60*60) # 30 days
      self.response.headers['Expires'] = (datetime.now() + timedelta(days=30)).strftime('%a, %d %b %Y %H:%M:%S GMT')
      self.response.headers["Content-Type"] = blob_info.content_type
      self.send_blob(blob_info)


class BlobDownloadPage(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, blob_key):
    blob_info = blobstore.get(blob_key)
    if not blob_info:
      self.error(404)
    else:
      self.response.headers["Cache-Control"] = "public, max-age="+str(30*24*60*60) # 30 days
      self.response.headers["Expires"] = (datetime.now() + timedelta(days=30)).strftime("%a, %d %b %Y %H:%M:%S GMT")
      self.response.headers["Content-Type"] = blob_info.content_type
      self.response.headers["Content-Disposition"] = str("attachment; filename=" + blob_info.filename)
      self.send_blob(blob_info)


class BlobInfoPage(handlers.BaseHandler):
  def get(self, blob_key):
    info = self._getBlobInfo(blob_key)
    if not info:
      self.error(404)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(info))

  def post(self, blob_key):
    info = self._getBlobInfo(blob_key)
    if not info:
      self.error(404)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(info))

  def _getBlobInfo(self, blob_key):
    blob_info = blobstore.get(blob_key)
    if not blob_info:
      return None

    size = None
    crop = None
    if self.request.POST.get('size'):
      size = int(self.request.POST.get('size'))
    if self.request.POST.get('crop'):
      crop = int(self.request.POST.get('crop'))

    return {'size': blob_info.size,
            'filename': blob_info.filename,
            'url': images.get_serving_url(blob_key, size, crop)}


class PicscanPage(BasePage):
  def get(self):
    self.render('picscan/index.html', {})


class PicscanPrivacyPage(BasePage):
  def get(self):
    self.render('picscan/privacy-policy.html', {})


class ShowcasePage(BasePage):
  def get(self):
    self.render('showcase.html', {})


class SitemapXmlPage(BasePage):
  def get(self):
    pages = []
    pages.append({
        "url": "//www.codeka.com/showcase",
        "lastmod": "2014-01-01",
        "priority": 1,
        "changefreq": "yearly"
      })

    query = (model.blog.Post.all()
                  .filter("isPublished", True)
                  .order('-posted'))
    for post in query:
      pages.append({
          "url": ("//www.codeka.com/blog/%04d/%02d/%s" %
                     (post.posted.year, post.posted.month, post.slug)),
          "lastmod": "%04d-%02d-%02d" % (post.updated.year, post.updated.month, post.updated.day),
          "priority": 10,
          "changefreq": "monthly"
        })

    self.render("sitemap.xml", {"pages": pages})


class SnipCreatePage(BasePage):
  def get(self):
    blobKey = self.request.GET.get('blob_key')
    if blobKey:
      snip = ctrl.snip.createSnip(blobKey)
      self.redirect('/snip/' + snip.slug)


class SnipNewPage(BasePage):
  def get(self):
    url = blobstore.create_upload_url('/blob/upload-complete')
    data = {'upload_url': url}
    self.render("snip-new.html", data)


class SnipPage(BasePage):
  def get(self, slug):
    snip = ctrl.snip.getSnip(slug)
    if not snip:
      self.error(404)
      return
    self.render("snip.html", {"snip": snip})


class SnipViewPage(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, slug):
    snip = ctrl.snip.getSnip(slug)
    if not snip:
      self.error(404)
      return
    self.response.headers["Cache-Control"] = "public, max-age="+str(30*24*60*60) # 30 days
    self.response.headers["Expires"] = (datetime.now() + timedelta(days=30)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    self.response.headers["Content-Type"] = snip.blob.content_type
    self.send_blob(snip.blob)


class NotFoundPage(BasePage):
  """This is the 404 "not found" page. We'll try to do some guesses as to what you may have wanted though."""
  def get(self):
    if "index.php?tempskin=" in self.request.path_qs:
      self.redirect("/blog/rss")
    elif "/blogs/" in self.request.path_qs:
      self.redirect(self.request.path_qs.replace("/blogs/", "/blog/"))
    elif "index.php" in self.request.path_qs:
      self.redirect("/")
    elif self.request.path == "/war-worlds/":
      self.redirect("http://www.war-worlds.com/") 
    else:
      self.error(404)


app = webapp.WSGIApplication([('/?', HomePage),
                              ('/blob/upload-url', BlobUploadUrlPage),
                              ('/blob/upload-complete', BlobUploadCompletePage),
                              ('/blob/([^/]+)', BlobPage),
                              ('/blob/([^/]+)/download', BlobDownloadPage),
                              ('/blob/([^/]+)/info', BlobInfoPage),
                              ('/picscan', PicscanPage),
                              ('/picscan/privacy-policy', PicscanPrivacyPage),
                              ('/showcase', ShowcasePage),
                              ('/sitemap.xml', SitemapXmlPage),
                              ('/snip/create', SnipCreatePage),
                              ('/snip/new', SnipNewPage),
                              ('/snip/([^/]+).png', SnipViewPage),
                              ('/snip/([^/]+)', SnipPage),
                              ('.*', NotFoundPage)],
                             debug=os.environ['SERVER_SOFTWARE'].startswith('Development'))
