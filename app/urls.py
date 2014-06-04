from django.conf.urls import patterns, include,url

#from study import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.views',
    url(r'^$','index'),
    )