import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch

import database
import utils.emails
from main import getDataLeaksByEmail, getLeakedEmailsByDomain

class Main_TestCases(unittest.TestCase):

  @patch.object(database.LeakedEmailsDB, 'get')
  def test_getDataLeaksByEmail_withReturn(self, mock_get):
    mockReturnValue = database.LeakedEmail('email@example.com', 'example.com', 'linkedin')
    expectedResult = {'dataLeaks': ['linkedin']}

    mock_get.return_value = [mockReturnValue]
    result = getDataLeaksByEmail('aa@aa.com')

    mock_get.assert_called_once_with(email='aa@aa.com')
    self.assertEqual(result, expectedResult)

  @patch.object(database.LeakedEmailsDB, 'get')
  def test_getDataLeaksByEmail_withoutReturn(self, mock_get):
    expectedResult = {'dataLeaks': []}

    mock_get.return_value = []
    result = getDataLeaksByEmail('bb@bb.com')

    mock_get.assert_called_once_with(email='bb@bb.com')
    self.assertEqual(result, expectedResult)

  @patch.object(database.LeakedEmailsDB, 'get')
  def test_getLeakedEmailsByDomain_withReturn(self, mock_get):
    mockReturnValue = database.LeakedEmail('email@example.com', 'example.com', 'neopets')
    expectedResult = {'emails': ['email@example.com']}

    mock_get.return_value = [mockReturnValue]
    result = getLeakedEmailsByDomain('cc@cc.com')

    mock_get.assert_called_once_with(domain='cc@cc.com')
    self.assertEqual(result, expectedResult)

  @patch.object(database.LeakedEmailsDB, 'get')
  def test_getLeakedEmailsByDomain_withoutReturn(self, mock_get):
    expectedResult = {'emails': []}

    mock_get.return_value = []
    result = getLeakedEmailsByDomain('dd@dd.com')

    mock_get.assert_called_once_with(domain='dd@dd.com')
    self.assertEqual(result, expectedResult)
    

class EmailUtils_TestCases(unittest.TestCase):

  def test_validateEmail_valid(self):
    result = utils.emails.validateEmail('email@example.com')
    self.assertEqual(result, True)

  def test_validateEmail_invalid(self):
    result = utils.emails.validateEmail('example.com')
    self.assertEqual(result, False)
    
  def test_getEmailDomain_success(self):
    result = utils.emails.getEmailDomain('email@example.com')
    self.assertEqual(result, 'example.com')

  def test_getEmailDomain_error(self):
    with self.assertRaises(ValueError) as context:
      utils.emails.getEmailDomain('email_no_domain')

    self.assertTrue('The provided email doesn\'t contain a domain' in str(context.exception))


class Database_TestCases(unittest.TestCase):

  def test_databaseInit_success(self):
    leakedEmail = database.LeakedEmail('email@example.com', 'example.com', 'neopets')
    db = database.LeakedEmailsDB([leakedEmail])

    self.assertEqual(db.lookups['email'].get('email@example.com', []), [0])
    self.assertEqual(db.lookups['domain'].get('eeee', []), [])
    self.assertEqual(db.lookups['company'].get('neopets', [1]), [0])

  def test_databaseInit_error(self):
    with self.assertRaises(ValueError) as context:
      database.LeakedEmailsDB([0, 1, 2])

    self.assertTrue('Provided leaked emails must be of type LeakedEmail' in str(context.exception))

  def test_databaseGet_success(self):
    leakedEmail = database.LeakedEmail('email@example.com', 'example.com', 'neopets')
    db = database.LeakedEmailsDB([leakedEmail])

    result = db.get(domain='example.com')

    self.assertEqual(result, (leakedEmail,))

  def test_databaseGet_noArgs(self):
    with self.assertRaises(ValueError) as context:
      db = database.LeakedEmailsDB([])
      db.get()
    
    self.assertTrue('One argument is needed for the get method' in str(context.exception))

  def test_databaseGet_wrontField(self):
    with self.assertRaises(ValueError) as context:
      db = database.LeakedEmailsDB([])
      db.get(banana='ba')
    
    self.assertTrue('Invalid field name' in str(context.exception))

if __name__ == '__main__':
  unittest.main()