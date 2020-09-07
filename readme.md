# Solution to Test 1: Recursive File Structure

A Python Flask web app using an SQLite database.

# Requirements
If requested I'll create an environment to include this app and a requirements.txt.
The moudles required by this app are as follows:
- python 3 (I used version 3.7.0)
- flask
- flask_wtf
- wtforms
- json
- sqlite3
- pathlib
- os
- sys

# Usage
- To run the app, navigate to the source directory and type: python app.pys
- If running locally, use URL localhost:5000 (127.0.0.1@5000)

# Folders

This contains two folders:
- source // the Python solution.
- tests // pytest test for the source code.

# source files
### app.py 
- The Flask app to run using Python
- Handles http requests, rendering templates
### database_manager.py
- Provides an interface to the database
### database_setup.py
- Creates/deletes the database; creates a 'paths' table
### path_interface.py
- A single interface for the App.py to call the logic to create the database from the text file and query its contents  
### tree_builder.py 
- Constructs a tree from the supplied text file and each node to write to the database. Creates a tree from the nodes stored in the database (that are returned in response to a query) and produces a list of the full path of each node.

# source/templates files
### base.html
- Provdes a base html file for the others to extend. Includes the navigation bar (so it does not need to be repeated on each page).
### home.html
- The base url page, proving information on the features provided by this web application 
### rest.html
 - A REST API to query the database and output results as JSON
### search.html
- Provides the main search page (web form), allowing the user to search the directory structure and present the results
# test files
### test_recursive_file_structure.py
- Calls into the path_interface.py, to delete and then create the database, from text file. Query's the database and tests for the expected results.
- To run tests, navigate to the test directory and type: pytest test_recursive_file_structure.py

# Data directory
### file_structure.txt
- A text file containing the recursive file structure which is read by this application.
### file_structure.db
- An SQLite databse file, created and populated by this application.

---
 ### Author
 - Neil Vine 2020
---
