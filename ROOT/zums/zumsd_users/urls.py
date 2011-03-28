from django.conf.urls.defaults import patterns, url
from fhurl import fhurl
from zums.zumsd_users.forms import LoginForm
from django.contrib.auth import views as django_auth_views

urlpatterns = patterns('zums.zumsd_users.views',
    fhurl(
        r'^login/$', template='zumsd_users/login.html',
        form_cls=LoginForm, next="/", name='auth_login'
    ),
    url(
        r'^logout/$', django_auth_views.logout, 
        {'template_name': 'zumsd_users/logout.html'}, name='auth_logout'
    ),
    url(r'^whoami/$', 'whoami'),
)
