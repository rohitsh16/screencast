from django.urls import path
from .controller import question
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('getQuestion', question.getQuestion, name='getQuestion'),
    path('checkAnswer', question.checkAnswer, name='checkAnswer'),
    path('leaderboard', question.leaderboard, name='leaderboard'),
    path('register', question.register, name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     