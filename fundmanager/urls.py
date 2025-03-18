from __future__ import annotations

from django.contrib import admin
from django.urls import include
from django.urls import path
from funds import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("fund", views.FundViewSet, basename="fund")


urlpatterns = [
    path("list/", views.IndexView.as_view()),
    path("upload/", views.UploadFileView.as_view()),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]
