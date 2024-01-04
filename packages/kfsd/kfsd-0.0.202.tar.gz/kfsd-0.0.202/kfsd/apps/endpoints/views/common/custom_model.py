from kfsd.apps.endpoints.views.common.model import ModelViewSet


class CustomModelViewSet(ModelViewSet):
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"
    ordering = ["-created"]

    def getPaginatedResponse(self, qs, serializer):
        page = self.paginate_queryset(qs)
        if page is not None:
            serializedData = serializer(page, many=True)
            return self.get_paginated_response(serializedData.data)
        serializedData = serializer(qs, many=True).data
        return serializedData
