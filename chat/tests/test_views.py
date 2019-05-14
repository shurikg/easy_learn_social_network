from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from chat.models import Message, MessageManager


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.outbox_url = reverse('chat:messages_outbox')
        self.inbox_url = reverse('chat:messages_inbox')

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

    def test_test_view(self):
        assert 1 == 1

    def test_outbox_view(self):
        response = self.client.post(self.outbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/outbox.html')

    def test_inbox_view(self):
        response = self.client.post(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/inbox.html')