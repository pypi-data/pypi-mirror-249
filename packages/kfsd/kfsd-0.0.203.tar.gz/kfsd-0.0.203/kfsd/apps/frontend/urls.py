from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.include_format_suffixes = False

urlpatterns = [
    path("", include(router.urls)),
    path("", include("kfsd.apps.frontend.collection.errors")),
]
