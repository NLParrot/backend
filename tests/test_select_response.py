import pytest

def test_get_response_valid(mock_open_toml, select_response):
    res = select_response.get_response("/some_path", {"name": "John"})
    assert res == "What are you doing, John?"

def test_get_response_without_variables(mock_open_toml_novar, select_response):
    res = select_response.get_response("/some_path")
    assert res == "No names required"

def test_get_response_variable_not_satisfied(mock_open_toml, select_response):
    res = select_response.get_response("/some_path")
    assert res == "Error while selecting response"


    

