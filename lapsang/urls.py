from django.contrib import admin
from django.urls import path
from tatoeba.views import GameList, GameDetail, GamePrepare, SentenceList, SentenceDetail


urlpatterns = [
    path('play', GameList.as_view()),
    path('play/<pk>', GameDetail.as_view(), name='game-detail'),
    path('play/<pk>/<lang>', GamePrepare.as_view(), name='game-prepare'),
    path('sentences/<lang>', SentenceList.as_view()),
    path('sentence/<pk>', SentenceDetail.as_view(),
         name='sentence-detail'),
    path('admin/', admin.site.urls),
]
