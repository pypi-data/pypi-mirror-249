from kfsd.apps.core.auth.api.gateway import APIGateway


class APIKeyAuth(APIGateway):
    def __init__(self, request=None):
        APIGateway.__init__(self, request)

    def getApiKeyUserInfo(self):
        apiKey = self.getAPIKey()  # noqa: F841
        return {}
