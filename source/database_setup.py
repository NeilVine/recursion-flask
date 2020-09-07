'''
database_setup.py 
  Create database file and a "paths" table 
'''

import sqlite3
import os

class Setup():
  '''
  A class to set up the database,
  including dding a 'paths' table
  '''

  def __init__(self, db_file_name):
    '''
    Creates a new Setup object 
    '''
    self.db_file_name = db_file_name

  def _database_exists(self):
    '''  
    Determine if the database file exists

    Returns: Ture if the file is found
    '''
    return os.path.exists(self.db_file_name) 

  def remove_database(self):
    '''  
    Delete the database file
    '''
    if self._database_exists():
      os.remove(self.db_file_name) 

  def create_paths_table(self, conn, cur ):
    '''
    Create table "paths"
    '''
    cur.execute("CREATE TABLE paths (name TEXT, parent INTEGER, id INTEGER PRIMARY KEY)")
