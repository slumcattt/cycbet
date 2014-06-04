from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cyc_bet.views.home', name='home'),
    url(r'^app/', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'app/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'template_name': 'app/index.html','next_page': '/app/'}),
)
