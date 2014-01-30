
import datetime
import os
import re
import webapp2 as webapp

import ctrl.blog
import handlers


class BlogPage(handlers.BaseHandler):
  pass


class HomePage(BlogPage):
  def get(self):
    pageNo = 0
    if self.request.get('page'):
      pageNo = int(self.request.get('page'))
    if pageNo < 0:
      pageNo = 0

    posts = ctrl.blog.getPosts(pageNo)
    if not posts and pageNo > 0:
      self.redirect('/blog?page=%d' % (pageNo-1))
    self.render('blog/index.html', {'posts': posts,
                                    'pageNo': pageNo})


class PostPage(BlogPage):
  def get(self, yearmonth, slug):
    year, month = yearmonth.split('/')
    year = int(year)
    month = int(month)
    post = ctrl.blog.getPostBySlug(year, month, slug)
    if not post:
      self.response.set_status(404)
      return
    self.render('blog/post.html', {'post': post})

  def head(self, yearmonth, slug):
    self.get(yearmonth, slug)
    self.response.body = ''


class RssPage(BlogPage):
  def get(self):
    posts = ctrl.blog.getPosts(0)
    pubDate = datetime.time()
    if posts:
      pubDate = posts[0].posted

    self.response.headers['Content-Type'] = 'application/rss+xml'
    self.render('blog/rss.xml', {'posts': posts,
                                 'pubDate': pubDate.strftime('%a, %d %b %Y %H:%M:%S GMT')})


class LegacyPage(BlogPage):
  def get(self, url):
    """This is used to redirect requests to the "new" page."""
    if url == "index.php":
      self.redirect("/blog")
      return
    elif url[:10] == "index.php/":
      # could be index.php/yyyy/mm/dd/slug so try to redirect it
      res = re.match(r"index\.php/([0-9]+)/([0-9]+)/[0-9]+/(.*)", url)
      if res:
        year = res.group(1)
        month = res.group(2)
        slug = res.group(3)
        self.redirect("/blog/" + year + "/" + month + "/" + slug)
        return
    self.error(404)


app = webapp.WSGIApplication([('/blog/?', HomePage),
                              ('/blog/([0-9]{4}/[0-9]{2})/(.*)', PostPage),
                              ('/blog/rss', RssPage),
                              ('/blog/(.*)', LegacyPage)],
                             debug=os.environ['SERVER_SOFTWARE'].startswith('Development'))
