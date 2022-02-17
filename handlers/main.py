from flask import Response, render_template

from model import blog
from . import handlers


@handlers.route('/')
def index():
  return render_template('index.html')


@handlers.route('/showcase')
def showcase():
  return render_template('showcase.html')


@handlers.route('/picscan')
def picscan():
  return render_template('picscan/index.html')


@handlers.route('/picscan/privacy-policy')
def picscan_privacy():
  return render_template('picscan/privacy-policy.html')


@handlers.route('/sitemap.xml')
def sitemap():
  pages = []
  pages.append({
      "url": "//www.codeka.com/showcase",
      "lastmod": "2022-02-16",
      "priority": 1,
      "changefreq": "yearly"
    })

  for f in blog.listPosts():
    post = blog.loadPost(f)
    pages.append({
        "url": ("//www.codeka.com/blog/%04d/%02d/%s" %
                    (post.posted.year, post.posted.month, post.slug)),
        "lastmod": "%04d-%02d-%02d" % (post.updated.year, post.updated.month, post.updated.day),
        "priority": 10,
        "changefreq": "monthly"
      })

  return Response(render_template("sitemap.xml", pages=pages), content_type="text/xml")
