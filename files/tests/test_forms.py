
from django.test import TestCase, Client
from files.forms import FilterFilesForm


class MyTests(TestCase):
    def setUp(self):
        self.form = FilterFilesForm({'1': '2'})

    def test_filterFilesForm_forms(self):
        form_data = {'something': 'something'}
        form = FilterFilesForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form(self):
        client = Client()
        response = client.post('/', {'filterFilesForm': 'something', 'filter_name': 'something'})
        self.assertEqual(response.status_code, 200)

    def test_sort_form(self):
        response1 = self.client.get("/")
        response2 = self.client.post("include url to post the data given", {'username': "testuser", 'category': "OOP", 'url': "files/media/files/test.pdf", 'owner': "test@test.com"})
        self.assertTrue('"error": true' , response2.content)
        self.assertEqual(response1.status_code, 200)
