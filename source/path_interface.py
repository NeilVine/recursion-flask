'''
path_interface.py
  An interface for the Flask App file to access features to  
  - setup and query the database
  - build a tree from a text file contents &
    write the tree to the database
    
 Provides the following
 - initialise function to read in the text file and create the database
 - query function to get required paths from the database
'''

import database_manager
from tree_builder import Directory_Tree
from pathlib import Path

class Path_Interface:
  '''
  Path_Interface - an interface for the Flask App to access functionality for:
    1. Reading in the text file containing a directory structure, and writing it to a database
    2. Querying the database for the existence of a named file or directory
  ''' 

  def __init__(self):
    '''
    Creates a new Path_Interface object
    '''
    txt_file = Path(__file__).parent / "data/file_structure.txt"
    self._tree = Directory_Tree(txt_file)
   
  def initialise(self):
    '''
    Create a database.
    Read in the directory structure from the text file.
    Store the paths in the database  
    '''
    # create the database
    database_manager.setup_database()
    # read in the directory structure and store in the database
    self._tree.create_tree_from_text_file()

  def query_database(self, name_to_find):  
    '''
    Query the database 

    Parameters: name_to_find - the name to search for

    Returns: The paths retrieved from the database
    '''
    results = None
    if name_to_find != None and name_to_find.strip() != "":
      results = self._tree.query_database_and_build_paths(name_to_find)
    if results is None or results == []:
      results = ["No matching files or directories found"]
    return results