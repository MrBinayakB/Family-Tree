from django.urls import path
from .views import RelationList, RelationDetail

urlpatterns = [
    path('relations/', RelationList.as_view(), name='relation-list'),
    path('relations/<int:pk>/', RelationDetail.as_view(), name='relation-detail'),
]
