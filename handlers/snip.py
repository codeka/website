import json
import logging
from flask import abort, redirect, render_template, request, send_file

import ctrl.snip
from . import handlers


@handlers.route('/snip/<slug>.png')
def snip_view(slug):
  filename = ctrl.snip.getSnipPath(slug)
  if filename == None:
    logging.warning("invalid slug: " + slug)
    abort(400)
  return send_file(filename, attachment_filename=slug + '.png', mimetype='image/png')


@handlers.route('/snip/<slug>')
def snip_page(slug):
  snip = ctrl.snip.getSnip(slug)
  return render_template('snip.html', snip=snip)


@handlers.route('/snip/upload', methods=['POST'])
def snip_upload():
  if 'file' not in request.files:
    abort(400)
  file = request.files['file']
  snip = ctrl.snip.saveSnip(file)
  if request.args.get('redirect') == '0':
    return json.dumps({'slug': snip.slug})
  else:
    return redirect('/snip/' + snip.slug)


@handlers.route('/snip/new')
def snip_new():
  return render_template('snip-new.html')

