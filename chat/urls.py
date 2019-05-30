from django.conf.urls import url
from django.views.generic import RedirectView

from chat.views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(permanent=True, url='inbox/'), name='messages_redirect'),
    url(r'^inbox/$', inbox, name='messages_inbox'),
    url(r'^outbox/$', outbox, name='messages_outbox'),
    url(r'^compose/$', compose, name='messages_compose'),
    url(r'^admin_message/$', compose_admin_message, name='messages_admin_compose'),
    #url(r'^compose/(?P<id>[\d]+)/$', compose, name='messages_compose'),
    url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    url(r'^reply/(?P<message_id>[\d]+)/$', reply, name='messages_reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', view, name='messages_detail'),
    url(r'^delete_inbox/(?P<message_id>[\d]+)/$', delete_inbox, name='message_delete_inbox'),
    url(r'^delete_outbox/(?P<message_id>[\d]+)/$', delete_outbox, name='message_delete_outbox'),
    #url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
    #url(r'^trash/$', trash, name='messages_trash'),
]