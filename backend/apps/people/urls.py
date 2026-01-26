from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('peoples/',views.people_list),
    path('peoples/<int:pk>',views.people_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)