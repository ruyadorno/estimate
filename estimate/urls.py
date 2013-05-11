import receivers #Activate the signal receivers, used on user registration
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'estimate.views.home', name='home'),
    url(r'^stories/', include('stories.urls')),
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^login/$', 'estimate.views.login_view', name='login'),
    url(r'^logout/$', 'estimate.views.logout_view', name='logout'),
    url(r'^user/(?P<user_id>\d+)$', 'estimate.views.user', name='user'),
    url(r'^groups/', 'estimate.views.groups', name='groups'),
    url(r'^add_group/', 'estimate.views.add_group', name='add_group'),
    url(r'^remove_group/', 'estimate.views.remove_group', name='remove_group'),
    url(r'^group/(?P<group_id>\d+)$', 'estimate.views.group', name='group'),
    url(r'^me/$', 'estimate.views.user_page', name='user_page'),
)
