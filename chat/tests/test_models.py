from django.test import TestCase
from chat.models import Message
from django.contrib.auth.models import User
import datetime


class TestModels(TestCase):

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

    def test_save_message(self):
        message = Message.objects.get(subject='test subject')
        self.assertIsNotNone(message)

    def test_sent_at_date(self):
        message_date = str(self.message.sent_at.date())
        date_now = str(datetime.datetime.now().date())
        self.assertEqual(message_date, date_now)
