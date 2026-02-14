from django.urls import path
from .views import PeopleList, PeopleDetail

urlpatterns = [
    path('people/', PeopleList.as_view(), name='people-list'),
    path('people/<int:pk>/', PeopleDetail.as_view(), name='people-detail'),
]
