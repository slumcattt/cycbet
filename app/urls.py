from django.conf.urls import patterns, include,url

#from study import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.views',
    url(r'^$','index'),
    url(r'^race/(?P<race_id>\d+)/$', 'race', name='race'),
    url(r'^stage/(?P<stage_id>\d+)/$', 'stage', name='stage'),
    url(r'^account$', 'account'),
    )