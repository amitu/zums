from django.conf.urls.defaults import patterns, url
from fhurl import fhurl
from zums.zumsd_users.forms import LoginForm, EmailOptionalRegistrationForm
from django.contrib.auth import views as auth_views

import zums

from zums.signals import UserSignedOut

def logout_with_signal(request, *args, **kw):
    user, sessionid = request.user, request.session.session_key
    resp = auth_views.logout(request, *args, **kw)
    UserSignedOut.send(sender=zums, user=user, sessionid=sessionid)
    return resp

urlpatterns = patterns('zums.zumsd_users.views',
    fhurl(
        r'^login/$', template='zumsd_users/login.html',
        form_cls=LoginForm, next="/", name='auth_login'
    ),
    fhurl(
        r'^register/$', template='zumsd_users/register.html',
        form_cls=EmailOptionalRegistrationForm, next="/", name='auth_register'
    ),
    url(
        r'^logout/$', logout_with_signal,
        {'template_name': 'zumsd_users/logout.html'}, name='auth_logout'
    ),
    url(r'^whoami/$', 'whoami'),
    url(
        r'^password/change/$', auth_views.password_change,
        name='auth_password_change',
        template_name="zumsd_users/password_change.html"
    ),
    url(
        r'^password/change/done/$', auth_views.password_change_done,
        name='auth_password_change_done',
    ),
    url(
        r'^password/reset/$', auth_views.password_reset,
        name='auth_password_reset'
    ),
    url(
        r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='auth_password_reset_confirm'
    ),
    url(
        r'^password/reset/complete/$', auth_views.password_reset_complete,
        name='auth_password_reset_complete'
    ),
    url(
        r'^password/reset/done/$', auth_views.password_reset_done,
        name='auth_password_reset_done'
    ),
)
