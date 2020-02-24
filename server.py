
import peeweedbevolve
from flask import Flask, render_template, request
from models import db # new line
app = Flask(__name__)

@app.before_request # new line
def before_request():
   db.connect()

@app.after_request # new line
def after_request(response):
   db.close()
   return response

@app.route("/")
def index():
   return render_template('index.html')
@app.cli.command() # new
def migrate(): # new 
   db.evolve(ignore_tables={'base_model'}) # new


if __name__ == '__main__':
   app.run()