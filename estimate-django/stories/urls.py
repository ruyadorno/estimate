from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'stories.views.index', name='stories_index'),
)
