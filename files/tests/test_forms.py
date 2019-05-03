
from django.test import TestCase, Client
from files.forms import filterFilesForm


class MyTests(TestCase):

    def test_filterFilesForm_forms(self):
        form_data = {'something': 'something'}
        form = filterFilesForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form(self):
        client = Client()
        response = client.post('/', {'filterFilesForm': 'something', 'filter_name': 'something'})
        self.assertEqual(response.status_code, 200)