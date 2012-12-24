from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'estimate.views.home', name='home'),
    url(r'^stories/', include('stories.urls')),
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^login/$', 'estimate.views.login_view', name='login'),
    url(r'^logout/$', 'estimate.views.logout_view', name='logout'),
)
