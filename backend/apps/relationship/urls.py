from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('relation/',views.relation_list),
    path('relation/<int:pk>',views.relation_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)