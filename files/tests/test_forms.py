from django.test import TestCase
from files.forms import filterFilesForm


class MyTests(TestCase):
    def test_filterFilesForm_forms(self):
        form_data = {'something': 'something'}
        form = filterFilesForm(data=form_data)
        self.assertTrue(form.is_valid())