from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.people.urls")),
    path("", include("apps.trees.urls")),
    path("", include("apps.relationship.urls")),
    path("", include("apps.users.urls")),
]
