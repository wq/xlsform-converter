import unittest
from xlsconv import xls2django, xls2html
from xlsconv.django import TEMPLATE_NAMES as django_templates
from xlsconv.html import TEMPLATE_NAMES as html_templates
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

    def check_django(self, name, ext):
        for template in django_templates:
            actual_python = xls2django(
                self.get_path('%s.%s' % (name, ext)),
                template,
            )
            expected_python = self.get_contents('%s/%s.py' % (name, template))
            self.assertEqual(expected_python, actual_python)

    def check_html(self, name, ext):
        for template in html_templates:
            actual_html = xls2html(
                self.get_path('%s.%s' % (name, ext)),
                template,
            )
            expected_html = self.get_contents('%s/%s.html' % (name, template))
            self.assertEqual(expected_html, actual_html)

    def test_input_types(self):
        self.check_django('input_types', 'xls')
        self.check_html('input_types', 'xls')

    def test_select(self):
        self.check_django('select', 'csv')
        self.check_html('select', 'csv')

    def test_repeat(self):
        self.check_django('repeat', 'csv')
        self.check_html('repeat', 'csv')

    def test_nestedfk(self):
        self.check_django('nestedfk', 'csv')
        self.check_html('nestedfk', 'csv')
