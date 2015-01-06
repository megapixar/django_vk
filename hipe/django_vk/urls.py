from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()
from imgs import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_vk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rtc/', include('rtc.urls')),
)
