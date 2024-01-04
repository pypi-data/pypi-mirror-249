from rest_framework.response import Response
from rest_framework import status

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet


class BaseHRelModelViewSet(CustomModelViewSet):
    def perform_create(self, serializer):
        request = self.request
        validated_data = serializer.validated_data
        if "created_by" not in validated_data:
            createdBy = None
            if request.token_user.isAuthenticated():
                createdBy = request.token_user.getUserId()
            elif hasattr(request, "api_key"):
                createdBy = request.api_key_user.getUserId()
            validated_data["created_by"] = createdBy
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
