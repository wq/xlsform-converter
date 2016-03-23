import unittest
from xlsconv import xls2django, xls2html
import os


class SurveyTestCase(unittest.TestCase):
    files_dir = os.path.join(os.path.dirname(__file__), 'files')
    maxDiff = None

    def get_path(self, filename):
        return os.path.join(self.files_dir, filename)

    def get_contents(self, filename):
        with open(self.get_path(filename)) as f:
            contents = f.read()
        return contents

    def check_html(self, name, ext='xls'):
        actual_html = xls2html(self.get_path('%s.%s' % (name, ext)))
        expected_html = self.get_contents('%s.html' % name)
        self.assertEqual(expected_html, actual_html)

    def check_django(self, name, ext='xls'):
        actual_python = xls2django(self.get_path('%s.%s' % (name, ext)))
        expected_python = self.get_contents('%s.py' % name)
        self.assertEqual(expected_python, actual_python)

    def test_input_type_html(self):
        self.check_html('input_types')

    def test_input_type_django(self):
        self.check_django('input_types')

    def test_select_html(self):
        self.check_html('select', 'csv')

    def test_select_django(self):
        self.check_django('select', 'csv')

    def test_repeat_html(self):
        self.check_html('repeat', 'csv')

    def test_repeat_django(self):
        self.check_django('repeat', 'csv')
