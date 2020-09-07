'''
database_manager.py
 - Provides an interface to the "file_structure" database.
'''

import sqlite3
from database_setup import Setup
from pathlib import Path

db_file_name = Path(__file__).parent / "data/file_structure.db"

def get_connection_and_cursor():
  '''
  Get a connection and a cursor
  '''
  conn = sqlite3.connect(db_file_name)
  c = conn.cursor() 
  return conn, c

def commit_and_close(conn):
  '''
  Commit and close the connection 
  '''
  conn.commit()
  conn.close()

def setup_database():
  '''
  Create the database, including a table to store the paths
  '''
  db_setup = Setup(db_file_name)
  # first remove the database 
  db_setup.remove_database()
  # create database again
  conn, c = get_connection_and_cursor()
  db_setup.create_paths_table(conn, c)
  commit_and_close(conn)

def add_path(path_to_add, parent, node_id):
  '''
  Add an entry to the "paths" table
  '''
  conn, c = get_connection_and_cursor()
  query = "INSERT INTO paths VALUES (?, ?, ?)" 
  c.execute(query, (path_to_add, parent, node_id))
  commit_and_close(conn)

def get_nodes_to_root(node_id):
  '''
  Query database to get paths containing the given 'path_name' 
 
  Parameters: 'node_id' the id of node to find 

  Returns: The records returned from the query
  '''
  conn, c = get_connection_and_cursor() 
  query = "SELECT * FROM paths WHERE id = ?" 
  c.execute(query, (node_id,))
  query_records = list(c)
  commit_and_close(conn)

  parent_id = query_records[0][1]
  if parent_id != -1:
    parents = get_nodes_to_root(parent_id)
    for rec in parents:
      query_records.append(rec)

  return query_records

def get_paths_named_like(path_name):
  '''
  Query database to get paths containing the given 'path_name' 
 
  Parameters: 'path_name' the name to serach for 

  Returns: The records returned from the query
  '''

  conn, c = get_connection_and_cursor()
  query = "SELECT * FROM paths WHERE name LIKE ?" 
  c.execute(query, (path_name + '%',))
  query_records = list(c)
  commit_and_close(conn)
  return query_records

def get_paths_and_parents(path_name):
  '''
  Get paths containing the given 'path_name' 
  
  Parameters: 'path_name' the name to search for within the paths

  Returns: the paths returned form the query and
           each path's parent back to the root   
  '''

  # query the database to get the paths
  initial_matches = get_paths_named_like(path_name)

  paths_and_parents = []
  parents = set()

  for record in initial_matches:
    paths_and_parents.append(record)
    record_parent_id = record[1]
    if len([x for x in initial_matches if x[2] == record_parent_id]) == 0:
      # parent is not present in the initial_matches 
      if record_parent_id != -1: # root node has parent of -1
        parents.add(record_parent_id)

  # now get each parent
  for parent in parents:
    paths = get_nodes_to_root(parent)
    for path in paths:
      paths_and_parents.append(path)

  return paths_and_parents, initial_matches

if __name__ == "__main__":
  # print what records get returnd from calling
  # get_paths_and_parent with the string 'image'
  paths = get_paths_and_parents("image")
  for path in paths:
    print(path)