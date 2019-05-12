from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import django
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from chat.models import Message


#if "pinax.notifications" in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    #from pinax.notifications import models as notification
#else:

notification = None

from chat.models import Message


def get_user_model():
    if django.VERSION[:2] >= (1, 5):
        from django.contrib.auth import get_user_model
        return get_user_model()
    else:
        from django.contrib.auth.models import User
        return User


def get_username_field():
    if django.VERSION[:2] >= (1, 5):
        return get_user_model().USERNAME_FIELD
    else:
        return 'username'


User = get_user_model()


class CommaSeparatedUserInput(widgets.Input):
    input_type = 'text'

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        elif isinstance(value, (list, tuple)):
            value = (', '.join([getattr(user, get_username_field()) for user in value]))
        return super(CommaSeparatedUserInput, self).render(name, value, attrs)


class CommaSeparatedUserField(forms.ChoiceField):
    #widget = CommaSeparatedUserInput

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        self._recipient_filter = recipient_filter
        super(CommaSeparatedUserField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(CommaSeparatedUserField, self).clean(value)
        if not value:
            return ''
        if isinstance(value, (list, tuple)):
            return value

        names = set(value.split(','))
        names_set = set([name.strip() for name in names if name.strip()])
        users = list(User.objects.filter(**{'%s__in' % get_username_field(): names_set}))
        unknown_names = names_set ^ set([getattr(user, get_username_field()) for user in users])

        recipient_filter = self._recipient_filter
        invalid_users = []
        if recipient_filter is not None:
            for r in users:
                if recipient_filter(r) is False:
                    users.remove(r)
                    invalid_users.append(getattr(r, get_username_field()))

        if unknown_names or invalid_users:
            raise forms.ValidationError(_(u"The following usernames are incorrect: %(users)s") % {
                'users': ', '.join(list(unknown_names) + invalid_users)})

        return users

    def prepare_value(self, value):
        if value is None:
            value = ''
        elif isinstance(value, (list, tuple)):
            value = (', '.join([getattr(user, get_username_field()) for user in value]))
        return value



'''
class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """

    def __init__(self, friends_list, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter
        self.friends_list = friends_list

    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"), max_length=140)
    body = forms.CharField(label=_(u"Body"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))


    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        for r in recipients:
            msg = Message(
                sender = sender,
                recipient = r,
                subject = subject,
                body = body,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = timezone.now()
                parent_msg.save()
            msg.save()
            message_list.append(msg)
            if notification:
                if parent_msg is not None:
                    notification.send([sender], "messages_replied", {'message': msg})
                    notification.send([r], "messages_reply_received", {'message': msg})
                else:
                    notification.send([sender], "messages_sent", {'message': msg})
                    notification.send([r], "messages_received", {'message': msg})
        return message_list

'''
class ComposeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        friends_list = kwargs.pop('friends_list', None)
        #is_reply = kwargs.pop('is_reply', None)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter
        super(ComposeForm, self).__init__(*args, **kwargs)
        self.fields['recipient'] = CommaSeparatedUserField(choices=tuple([(name, name) for name in friends_list]))
        self.fields['subject'] = forms.CharField(label=_(u"Subject"), max_length=140)
        self.fields['body'] = forms.CharField(label=_(u"Body"), widget=forms.Textarea(attrs={'rows': '12', 'cols': '55'}))

    def save(self, sender, parent_msg=None):
        print("save rec   ",self.fields['recipient'])
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        for r in recipients:
            print(r)
            print(type(r))
            msg = Message(
                sender=sender,
                recipient=r,
                subject=subject,
                body=body,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = timezone.now()
                parent_msg.save()
            msg.save()
            message_list.append(msg)
            if notification:
                if parent_msg is not None:
                    notification.send([sender], "messages_replied", {'message': msg})
                    notification.send([r], "messages_reply_received", {'message': msg})
                else:
                    notification.send([sender], "messages_sent", {'message': msg})
                    notification.send([r], "messages_received", {'message': msg})
        return message_list

    class Meta:
        model = Message
        fields = ('recipient', 'subject', 'body')