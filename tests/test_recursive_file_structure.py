'''
Tests for the recursive file structure solution
'''

import pytest
import sys
sys.path.append("../source")
from path_interface import Path_Interface

def test_Search_for_none():
    '''
    Test that a search for None returns an empty list
    '''
    pi = Path_Interface()
    pi.initialise()
    query = None
    result = pi.query_database(query)
    assert result == ['No matching files or directories found']

def test_search_for_empty_string():
    '''
    Test that a search for an empty empty string returns an empty list
    '''
    pi = Path_Interface()
    pi.initialise()
    query = ""
    result = pi.query_database(query)
    assert result == ['No matching files or directories found']
    
def test_search_for_youtube():
    '''
    Test that a search for 'YouTube' returns an empty list
    '''
    pi = Path_Interface()
    pi.initialise()
    query = 'YouTube'
    result = pi.query_database(query)
    assert result == ['No matching files or directories found'] 

def test_search_for_image():
    '''
    Test that a search for 'image' returns a list containing three files and a directory
    as specified in the assert 
    '''
    pi = Path_Interface()
    pi.initialise()
    query = 'image'
    result = pi.query_database(query)
    assert result == ['C:\\Documents\\Images\\Image1.jpg', 'C:\\Documents\\Images\\Image2.jpg', 'C:\\Documents\\Images\\Image3.png', 'C:\\Documents\\Images']


def test_search_for_skpye():
    '''
    Test that a search for 'skype' returns a list containing one file and a folder
    as specified in the assert
    '''
    pi = Path_Interface()
    pi.initialise()
    query = 'skype'
    result = pi.query_database(query)
    assert result == ['C:\\Program\tFiles\\Skype\\Skype.exe', 'C:\\Program\tFiles\\Skype']
