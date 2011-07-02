from django.conf.urls.defaults import patterns, url
from fhurl import fhurl
from zums.zumsd_users.forms import LoginForm
from django.contrib.auth import views as django_auth_views

import zums

from zums.signals import UserSignedOut

def logout_with_signal(request, *args, **kw):
    user, sessionid = request.user, request.session.session_key
    resp = django_auth_views.logout(request, *args, **kw)
    UserSignedOut.send(sender=zums, user=user, sessionid=sessionid)
    return resp

urlpatterns = patterns('zums.zumsd_users.views',
    fhurl(
        r'^login/$', template='zumsd_users/login.html',
        form_cls=LoginForm, next="/", name='auth_login'
    ),
    url(
        r'^logout/$', logout_with_signal,
        {'template_name': 'zumsd_users/logout.html'}, name='auth_logout'
    ),
    url(r'^whoami/$', 'whoami'),
)
