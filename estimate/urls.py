from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'estimate.views.home', name='home'),
    url(r'^stories/', include('stories.urls')),
    url(r'^openid/', include('django_openid_auth.urls')),
)
