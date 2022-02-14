from flask import render_template

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
  