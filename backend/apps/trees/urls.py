from django.urls import path
from .views import TreeList, TreeDetail

urlpatterns = [
    path('trees/', TreeList.as_view(), name='tree-list'),
    path('trees/<int:pk>/', TreeDetail.as_view(), name='tree-detail'),
]
