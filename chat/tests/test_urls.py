from django.test import TestCase
from django.urls import reverse, resolve
from chat.views import *

class TestUrls(TestCase):

    def setUp(self):

        # create sender
        recipient_username = 'sender'
        recipient_email = 'sender@test.com'
        recipient_password = '12345'
        self.sender = User(username=recipient_username, email=recipient_email)
        self.sender.set_password(recipient_password)
        self.sender.save()
        login = self.client.login(username=recipient_username, password=recipient_password)
        self.assertEqual(login, True)

        # create recipient
        recipient_username = 'recipient'
        recipient_email = 'recipient@test.com'
        recipient_password = '12345'
        self.recipient = User(username=recipient_username, email=recipient_email)
        self.recipient.set_password(recipient_password)
        self.recipient.save()
        login = self.client.login(username=recipient_username, password=recipient_password)
        self.assertEqual(login, True)

        # create message
        self.message = Message.objects.create(
            subject='test subject',
            body='test body',
            sender=self.sender,
            recipient=self.recipient,
        )

    def test_test_url_is_resolved(self):
        assert 1 == 1

    def test_message_inbox_url_is_resolved(self):
        url = reverse('chat:messages_inbox')
        self.assertEqual(resolve(url).func, inbox)

    def test_message_compose_url_is_resolved(self):
        url = reverse('chat:messages_compose')
        self.assertEqual(resolve(url).func, compose)


