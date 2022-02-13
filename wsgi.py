from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/showcase')
def showcase():
  return render_template('showcase.html')