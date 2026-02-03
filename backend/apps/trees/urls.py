from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('tree/',views.tree_list),
    path('tree/<int:pk>',views.tree_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)