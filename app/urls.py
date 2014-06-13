from django.conf.urls import patterns, include,url

#from study import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.views',
    url(r'^$','index'),
    url(r'^race/(?P<race_id>\d+)/$', 'race', name='race'),
    url(r'^stage/(?P<stage_id>\d+)/$', 'stage', name='stage'),
    url(r'^add_to_betslip/$', 'add_to_betslip'),
    url(r'^remove_from_betslip/$', 'remove_from_betslip'),
    url(r'^account$', 'account'),
    )