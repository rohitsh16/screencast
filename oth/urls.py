from django.conf.urls import url

from oth import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^answer/$', views.answer , name='answer'),
    url(r'^lboard/$', views.lboard , name='lboard'),
    url(r'^rules/$', views.rules , name='rules'),
    url(r'^api/player$', views.PlayerList.as_view(),name='api'),
    url(r'^api/qgroup1$', views.LevelList1.as_view(),name='api'),
    url(r'^api/qgroup2$', views.LevelList2.as_view(),name='api'),
    url(r'^api/qgroup3$', views.LevelList3.as_view(),name='api'),
     url(r'^api/leaderboard/$',views.lboard_api,name='lboard_api'),
]
