from django.conf.urls import url

from oth import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^answer/$', views.answer , name='answer'),
    url(r'^lboard/$', views.lboard , name='lboard'),
    url(r'^rules/$', views.rules , name='rules'),
]
