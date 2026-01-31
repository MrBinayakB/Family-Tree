from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("peoples/", include("apps.people.urls")),
    path("trees/", include("apps.trees.urls")),
    path("relationship/", include("apps.trees.urls")),
    path("users/", include("apps.trees.urls")),
]
