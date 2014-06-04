from django.conf.urls import patterns, include,url

#from study import views

urlpatterns = patterns('app.views',
    url(r'^$','index'),
    )