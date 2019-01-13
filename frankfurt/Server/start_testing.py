import unittest
from FlaskServer_WITH_POOL import app
from base64 import b64encode

class MyTestClass(unittest.TestCase):

  # initialization logic for the test suite declared in the test module
  # code that is executed before all tests in one test run
  @classmethod
  def setUpClass(cls):
       pass

  # clean up logic for the test suite declared in the test module
  # code that is executed after all tests in one test run
  @classmethod
  def tearDownClass(cls):
       pass

  # initialization logic
  # code that is executed before each test
  def setUp(self):
      self.app = app.test_client()
      self.app.testing = True

  # clean up logic
  # code that is executed after each test
  def tearDown(self):
    pass

  # test method
  def test_login(self):
      headers = {'Authorization': 'Basic ' + b64encode("fatihgulmez:12345")}

      result = self.app.get("/organizations/istanbul_sehir_university/fcgtyg", headers=headers)
      return self.assertEqual(result.status_code, 200)
      pass

# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()