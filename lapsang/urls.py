from django.contrib import admin
from django.urls import path
from tatoeba.views import SentenceDetail, SentenceList


urlpatterns = [
    path('play', SentenceList.as_view()),
    path('sentences/<lang>', SentenceList.as_view()),
    path('sentence/<pk>', SentenceDetail.as_view(),
         name='sentence-detail'),
    path('admin/', admin.site.urls),
]
