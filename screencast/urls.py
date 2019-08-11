from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('quiz/', include('quiz.urls')),
    path('admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls')) #Django REST framework browsable api(Opt.)
]
