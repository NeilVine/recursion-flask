'''
app.py the Python Flask App solution to the Recursive File Structure test
  - creates Flask instance and runs it
  - presents tempalte HTML pages to front end
'''

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import request
import json
from path_interface import Path_Interface

# create an instance of Flask
app = Flask(__name__)
# Prior to deployment create a unique id for this app (store it in config) 
app.config['SECRET_KEY'] = 'TODO'

# Create an instance of the Path_Interface  
__pi = Path_Interface()
# Initialise the app 
# - read in directory structure from text file
# - store the file structure in the database
__pi.initialise()

def query_database(query):
  '''
  Query/search the database

  Parameters: 'query' the values to search for

  Returns: The results to display obtained from the database
  '''
  global __pi
  if __pi is None:
    __pi = Path_Interface()
  return __pi.query_database(query)

# form for querying the database, for the presence of a file or directory
class QueryForm(FlaskForm):
    query = StringField("Search for file or directory")
    submit = SubmitField("Submit")

#route home page
@app.route('/')
def index():
  return render_template('home.html')

#route search page
@app.route('/search', methods=['GET','POST'])
def search_page():
  form = QueryForm()
  query = ""
  result = ""

  if form.validate_on_submit():
    query = form.query.data
    form.query.data = ""
    # query the database for results
    result = query_database(query)
      
  return render_template('search.html', form=form,query=query, result=result)

#route rest page
@app.route('/rest')
def rest_page():
  search = request.args.get('search')
  if not search:
    return render_template("rest.html")

  # query the database for results
  result = query_database(search)
  json_object = json.dumps(result, indent = 4)
  return json_object

if __name__ == '__main__':
  # using debug mode whilst developing
  app.run(debug=True)

