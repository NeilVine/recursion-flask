'''
tree_builder.py provides:
  1. A 'Node' class to hold a directory or file
  2. A 'Directory_Tree' for building a tree
    -  building a tree from the text file
    -  building a tree from the records stored in the database
    -  processing the tree in response to a query and return data to display to a user
'''

import database_manager

class Node():
  '''
  A class representing a node in a directory structure
  '''

  def __init__(self, name, parent, id, level):
    '''
    Creates a new instance of the Node class

    Parameters:
      - name: The name of this node in the directory structure
      - parent: The id of the parent of this node in the directory structure
      - id: A unique id for this node
    '''
    self.name = name
    self.parent = parent
    self.id = id
    self.children = []
    self.level = level

class Directory_Tree():
  '''
  A class representing a file structure  
  '''

  def __init__(self, text_file):
    '''
    Creates a new instance of the Directory_Tree class

    Parameters: text_file - the text file containing the directory structure
    '''
    self.text_file = text_file
    self.next_node_number = 0
    self.tree_root = None
    self.current_parent = None
  
  def _get_level(self, line):
    '''
    Determine the depth of the node using the indentation 

    Returns: The level of the node in the tree with zero being the root
    '''
    indent = len(line) - len(line.lstrip())
    level = 0
    if indent > 0:
      level = indent / 7
    return level

  def _get_parent(self, level):
    '''
    Determine the parent of the node about to be created

    Parameters: Level - the level of the node in the tree

    Returns: The parent node
    '''
    if level == 0:
      return None # node is the root
    if level == 1:
       return self.tree_root # node is child of the root

    # if the new node's level is not one more than that of the node
    # pointed to by current_parent, move up one generation and try that
    while level < self.current_parent.level + 1:
        self.current_parent = self.current_parent.parent  

    return self.current_parent

  def _add_node(self, parent, name, level):
    '''
    Add a node to the tree

    Returns: The newly created node
    '''
    node = Node(name, parent, self.next_node_number, level)
    if parent == None:
      self.tree_root = node
    self.next_node_number += 1
    return node

  def _process_line(self, line):
    '''
    Process a line from the text file representing a directory structure.
    - Create a node 
    - Add the child to its parent

    Parameters: 'line' a line from the text file
    '''
    level = self._get_level(line)
    parent = self._get_parent(level)
    name = line.strip()
    node = self._add_node(parent, name, level)
    self.current_parent = node
    if parent != None:
      parent.children.append(node)

  def _write_node_to_database(self, node):
    '''
    Create a database record representing the passed in node
    and recursively call this function with each of this node's children

    Parameters: node, the node to represent in a database entry
    '''
    parent_id = -1
    if node.parent != None:
      parent_id = node.parent.id

    database_manager.add_path(node.name, parent_id, node.id)
    for child in node.children:
      self._write_node_to_database(child)

  def create_tree_from_text_file(self):
    '''
    Using the directory structure specified in the text file
    create a tree structure representation of it 
    and store it in a database
    ''' 
    
    # process the file line by line, creating a tree
    with open(self.text_file, 'r') as fp:
      for line in fp:
        if len(line.strip()) > 0:
          self._process_line(line)

    # write the tree to the database
    if self.tree_root != None:
      self._write_node_to_database(self.tree_root)
    else:
      print("Failed to write to DB as self.tree_root is None")

  def _add_children_from_db_records(self, node, records):
    '''
    Add child nodes to 'node', using the information in 'records'

    Parameters:
            - 'node' the node to add children to
            - 'records' database records, containing node information

    Returns: The constructed tree 
    '''

    # locate children
    for rec in records:
      if rec[1] == node.id:
        # found a child 
        child = Node(rec[0], rec[1], rec[2] , node.level + 1)
        node.children.append(child)
        self._add_children_from_db_records(child,records)

    return node # node with all children added recursively

  def _create_tree_from_db_records(self, records):
    '''
    Create a tree from the supplied database records

    Parameters: 'records' the records from the database table

    Returns: The Root of the created tree            
    '''
    
    root = None
    root_index = -1
    tree = None
    
    # identify the root node
    for index in range(0,len(records)):
      rec = records[index]
      if rec[1] == -1:
        root_index = index
        root = Node(rec[0], rec[1], rec[2] , 0)
        break
    
    if root != None:
      tree = self._add_children_from_db_records(root,records)
     
    return tree

  def _get_leaf_nodes(self, node):
    '''
    Find the leaf nodes

    Parameters: 'node' the tree to get the leaf nodes from 

    Returns: The leaf nodes
    '''
    leafs = []

    if node.children is None or len(node.children) == 0:
      leafs.append(node)
    else:
      for child in node.children:
        leafs.extend(self._get_leaf_nodes(child))

    return leafs

  def _get_full_path_to_node(self, leaf, tree_dict):
    '''
    Construct the full path to the node 

    Parameters:
            - 'leaf' the leaf node to get the full path for
            - 'tree_dict' the tree stored as a dictionary 

    Returns: The full path from route to the leaf
    '''
    full_path = ""
  
    node_name = leaf[0]
    node_parent = leaf[1]
    node_id = leaf[2]

    if node_parent == -1:
      return node_name

    full_path = "\\" + node_name
    
    while node_parent != -1:
      if tree_dict.get(node_parent) != None:
        item = tree_dict[node_parent]
        node_name = item[0]
        node_parent = item[1]
        node_id = item[2]
        if node_parent == -1:
          full_path = full_path[1:] #remove leading backslash
          full_path = node_name + full_path
        else:
          full_path = "\\" + node_name + full_path
      else:
        print(f"node id {node_parent} was not found in dictionary")
        break

    return full_path

  def _create_list_from_tree(self, tree, tree_dict):
    '''
    Create a list of paths (one per leaf node) 

    Paramters: 
          - 'tree' the tree to convert
          - 'tree_dict' a dictionary of tree nodes
    Returns: A list of paths of leaves, to display to the user
    '''
    path_list = []

    # start by creating a list item for each leaf
    leafs = self._get_leaf_nodes(tree)
    
    # get the full path for each image
    for leaf in leafs:    
      path_list.append(self._get_full_path_to_node(tree_dict[leaf.id], tree_dict))

    return path_list, leafs

  def _create_dictionary(self, records):
    '''
    Create a dictionary of the tree nodes dict<node id, node>

    Parameters: 'records' database records representing nodes

    Returns: The dictionary of nodes
    '''
    tree_dict = {}
    for rec in records:
      tree_dict[rec[2]] = rec
    return tree_dict

  def _create_list_of_non_leaf_matches(self, non_leaf_matches, tree, tree_dict):
    '''
    Create a list of the full paths of non-leaf nodes

    Parameters:
          - 'non_leaf_matches' the nodes whose full paths are to be determined
          - 'tree' the tree 
          - 'tree_dict' a dictionary of tree nodes

    Returns: A list of full paths to each node contained in the 'non_leaf_matches' parameter
    '''
    full_paths = []

    for match in non_leaf_matches:
      node_id = match[2]
      node = tree_dict[node_id]
      full_paths.append(self._get_full_path_to_node(node, tree_dict))

    return full_paths


  def query_database_and_build_paths(self, name_to_find):
    '''
    Query the database for records named similar to 'name_to_find',
    Build a list containing the full path for each leaf (file or empty dir)

    Parameters: 'name_to_find' the name to find (search for) in the database of paths  

    Returns: A list of full paths, to display to a user
    '''
    
    display_list = []
   
    # initial_matches => the records matching the name_to_find
    # matching_records_to_root => records representing nodes back to the root
    matching_records_to_root, initial_matches = database_manager.get_paths_and_parents(name_to_find)

    if len(initial_matches) > 0:

      # tree_dict => dictionary of the matching records back to the root
      tree_dict = self._create_dictionary(matching_records_to_root)

      # tree => a directory tree structure - contains items recieved from searching the database
      tree = self._create_tree_from_db_records(matching_records_to_root)

      # leafs => the tree's leaves 
      # display_list => a list of full paths to each leaf 
      display_list, leafs = self._create_list_from_tree(tree, tree_dict)

      # create a list of non-leaf matches 
      leaf_node_ids = []
      for node in leafs:
        leaf_node_ids.append(node.id)
      non_leaf_matches = [f for f in initial_matches if f[2] not in leaf_node_ids]

      if len(non_leaf_matches) > 0:
        # get a list of full paths to each non-leaf match
        non_leaf_display_list = self._create_list_of_non_leaf_matches(non_leaf_matches, tree, tree_dict)
        # add these paths to the display_list
        display_list.extend(non_leaf_display_list)
   
    return display_list # list of full paths for each matching node 