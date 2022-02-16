import logging
from flask import abort, render_template, send_file

import ctrl.snip

from . import handlers



@handlers.route('/snip/<slug>.png')
def snip_view(slug):
  filename = ctrl.snip.getSnipPath(slug)
  if filename == None:
    logging.warning("invalid slug: " + slug)
    abort(400)
  return send_file(filename, attachment_filename=slug + '.png', mimetype='image/png')
