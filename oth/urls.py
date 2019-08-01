from django.conf.urls import url

from oth import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^answer/$', views.answer , name='answer'),
    url(r'^lboard/$', views.lboard , name='lboard'),
    url(r'^rules/$', views.rules , name='rules'),
    url(r'^api/player$', views.PlayerList.as_view(),name='api'),
    url(r'^api/level$', views.LevelList.as_view(),name='api'),
     url(r'^api/leaderboard/$',views.lboard_api,name='lboard_api'),
]
