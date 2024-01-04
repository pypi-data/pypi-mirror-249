from django.urls import path

from kfsd.apps.frontend.views.errors.custom403 import Custom403View
from kfsd.apps.frontend.views.errors.custom404 import Custom404View
from kfsd.apps.frontend.views.errors.custom500 import Custom500View

urlpatterns = [
    path("errors/forbidden/", Custom403View.as_view(), name="forbidden"),
    path("errors/notfound/", Custom404View.as_view(), name="notfound"),
    path("errors/error/", Custom500View.as_view(), name="error"),
]
