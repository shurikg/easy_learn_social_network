from django.contrib.auth.decorators import login_required
from chat.models import Message
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from chat.forms import ComposeForm, get_user_model, get_username_field
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.text import wrap
from django.contrib import messages
from django.urls import reverse

User = get_user_model()


def format_quote(sender, body):
    """
    Wraps text at 55 chars and prepends each
    line with `> `.
    Used for quoting messages in replies.
    """
    lines = wrap(body, 55).split('\n')
    for i, line in enumerate(lines):
        lines[i] = "> %s" % line
    quote = '\n'.join(lines)
    return ugettext(u"%(sender)s wrote:\n%(body)s") % {
        'sender': sender,
        'body': quote
    }


@login_required
def inbox(request, template_name='chat/inbox.html'):
    """
    Displays a list of received messages for the current user.
    Optional Arguments:
        ``template_name``: name of the template to use.
    """
    message_list = Message.objects.inbox_for(request.user)
    return render(request, template_name, {
        'message_list': message_list,
    })


@login_required
def outbox(request, template_name='chat/outbox.html'):
    """
    Displays a list of sent messages by the current user.
    Optional arguments:
        ``template_name``: name of the template to use.
    """
    message_list = Message.objects.outbox_for(request.user)
    return render(request, template_name, {
        'message_list': message_list,
    })


@login_required
def view(request, message_id, form_class=ComposeForm, quote_helper=format_quote,
         subject_template=_(u"Re: %(subject)s"),
         template_name='chat/view.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either
    the sender or the recipient. If the user is not allowed a 404
    is raised.
    If the user is the recipient and the message is unread
    ``read_at`` is set to the current datetime.
    If the user is the recipient a reply form will be added to the
    tenplate context, otherwise 'reply_form' will be None.
    """
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()

    context = {'message': message, 'reply_form': None}
    #if message.recipient == user:
        #form = form_class(initial={
            #'body': quote_helper(message.sender, message.body),
            #'subject': subject_template % {'subject': message.subject},
            #'recipient': [message.sender,]
            #})
        #context['reply_form'] = form
    return render(request, template_name, context)


@login_required
def reply(request, message_id, form_class=ComposeForm,
          template_name='chat/compose.html', success_url=None,
          recipient_filter=None, quote_helper=format_quote,
          subject_template=_(u"Re: %(subject)s"),):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.
    """
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        #form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('chat:messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial={
            'body': quote_helper(parent.sender, parent.body),
            'subject': subject_template % {'subject': parent.subject},
            'recipient': [parent.sender,]
            })
    return render(request, template_name, {
        'form': form,
    })


@login_required
def compose(request, recipient=None, form_class=ComposeForm,
            template_name='chat/compose.html', success_url=None,
            recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    is_staff = request.user.is_staff
    users = User.objects.all()
    users_list = ''
    for u in users:
        users_list += u.username
        users_list += ','
    users_list[:-1]

    if not is_staff:
        friends_list = request.user.profile.friends.all()
        users_list = []
        for friend in friends_list:
            users_list.append(friend.user)

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, friends_list=users_list, recipient_filter=recipient_filter, is_staff=is_staff)
        #form = form_class(request.POST, '')
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('chat:messages_inbox')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(friends_list=users_list, is_staff=is_staff)
        if recipient is not None:
            recipients = [u for u in User.objects.filter(**{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
            form.fields['recipient'].initial = recipients
    return render(request, template_name, {'form': form,})