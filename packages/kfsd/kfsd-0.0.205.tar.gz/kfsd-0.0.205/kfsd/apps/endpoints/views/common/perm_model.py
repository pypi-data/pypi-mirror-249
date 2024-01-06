from rest_framework.response import Response
from rest_framework import status

from kfsd.apps.endpoints.views.common.model import ModelViewSet
from kfsd.apps.core.auth.token import TokenUser
from kfsd.apps.core.exceptions.api import KubefacetsAPIException


class PermModelViewSet(ModelViewSet):
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"

    def getModelName(self):
        return self.queryset.model._meta.verbose_name

    def isPermEnabled(self, request):
        if (
            self.request.token_user.isAuthEnabled()
            and self.request.token_user.isAuthenticated()
        ):
            return True
        return False

    def getUser(self, request) -> TokenUser:
        return self.request.token_user

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.isPermEnabled(self.request):
            user = self.getUser(self.request)
            resp = user.has_perm_all_resources("can_view", self.getModelName())
            return queryset.filter(identifier__in=resp)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if self.isPermEnabled(self.request):
            if not self.getUser(self.request).isAuthenticated():
                raise KubefacetsAPIException(
                    "Permission Denied",
                    "permission_denied",
                    status.HTTP_401_UNAUTHORIZED,
                )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.isPermEnabled(self.request):
            user = self.getUser(self.request)
            if not user.has_perm("can_edit", instance):
                raise KubefacetsAPIException(
                    "Permission Denied",
                    "permission_denied",
                    status.HTTP_401_UNAUTHORIZED,
                )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.isPermEnabled(self.request):
            user = self.getUser(self.request)
            if not user.has_perm("can_delete", instance):
                raise KubefacetsAPIException(
                    "Permission Denied",
                    "permission_denied",
                    status.HTTP_401_UNAUTHORIZED,
                )
        instance.delete()
        return Response({}, status.HTTP_204_NO_CONTENT)
