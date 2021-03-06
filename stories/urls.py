from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'stories.views.index', name='stories_index'),
    url(r'^add/', 'stories.views.add_project', name='stories_add_project'),
    url(r'^remove/', 'stories.views.remove_project', name='stories_remove_project'),
    url(r'^project/(?P<project_id>\d+)/$', 'stories.views.project_page', name='project_page'),
    url(r'^change_story_time/$', 'stories.views.change_story_time', name='change_story_time'),
    url(r'^add_story/$', 'stories.views.add_story', name='add_story'),
    url(r'^remove_story/$', 'stories.views.remove_story', name='remove_story'),
    url(r'^edit_story/$', 'stories.views.edit_story', name='edit_story'),
    url(r'^update_order/$', 'stories.views.update_order', name='update_order'),
)
