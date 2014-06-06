from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

#for serving images
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.index', name='home'),
    url(r'^app/', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'app/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'template_name': 'app/index.html','next_page': '/app/'}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
