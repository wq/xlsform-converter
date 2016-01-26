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
            contents = f.read().strip()
        return contents

    def test_html(self):
        expected_html = self.get_contents('expected_form.html')
        actual_html = xls2html(self.get_path('survey.xls')).strip()
        self.assertEqual(expected_html, actual_html)

    def test_django(self):
        expected_python = self.get_contents('expected_models.py')
        actual_python = xls2django(self.get_path('survey.xls')).strip()
        self.assertEqual(expected_python, actual_python)
