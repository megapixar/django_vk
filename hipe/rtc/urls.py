from django.conf.urls import patterns, url
from rtc import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^offer/', views.offer, name='offer'),
   url(r'^answer/', views.answer, name='answer'),
   url(r'^get_offer/', views.get_offer, name='get_offer'),
   url(r'^get_answer/', views.get_answer, name='get_answer'),
   url(r'^candidate/', views.candidate, name='candidate'),
   url(r'^one_tab/', views.one_tab, name='one_tab'),
   )