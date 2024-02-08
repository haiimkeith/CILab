"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

# test_counter.py

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app, COUNTERS

# we need to import the file that contains the status codes
from src import status 


class CounterTest(TestCase):
  """Counter tests"""

  def test_create_a_counter(self):
    """It should create a counter"""
    client = app.test_client()
    result = client.post('/counters/foo')
    self.assertEqual(result.status_code, status.HTTP_201_CREATED)
  
  
  def setUp(self):
    self.client = app.test_client()

  def test_duplicate_a_counter(self):
    """It should return an error for duplicates"""
    result = self.client.post('/counters/bar')
    self.assertEqual(result.status_code, status.HTTP_201_CREATED)
    result = self.client.post('/counters/bar')
    self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)


  def test_update_a_counter(self):
    result = self.client.post('/counters/abc')
    self.assertEqual(result.status_code, status.HTTP_201_CREATED)
    self.assertEqual(result.json['abc'], 0)

    result = self.client.put('/counters/abc')
    self.assertEqual(result.status_code, status.HTTP_200_OK)
    self.assertEqual(result.json['abc'], 1)

  def test_get_a_counter(self):
    result = self.client.post('/counters/kdr')
    self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    result = self.client.get('/counters/kdr')
    self.assertEqual(result.status_code, status.HTTP_200_OK)

    result = self.client.get('/counters/doesntexist')
    self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

  def test_delete_a_counter(self):
    result2 = self.client.delete('/counters/randomdelete')
    self.assertEqual(result2.status_code, status.HTTP_404_NOT_FOUND)
    result = self.client.post('/counters/del')
    self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    result = self.client.delete('/counters/del')
    self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)