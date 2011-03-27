from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^session-test/', 'zums_jd_test_project.views.session_test'),
)
