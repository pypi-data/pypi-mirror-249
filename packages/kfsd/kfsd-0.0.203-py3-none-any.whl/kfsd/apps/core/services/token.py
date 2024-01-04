from rest_framework import status
from kfsd.apps.core.common.logger import Logger, LogLevel

# from kfsd.apps.core.common.cache import cache
from kfsd.apps.core.services.base import BaseRequest

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class TokenApi(BaseRequest):
    def __init__(self, request=None):
        BaseRequest.__init__(self, request)

    def getLogoutUrl(self):
        return self.constructUrl(
            [
                "services.context.mgmt_api.host",
                "services.context.mgmt_api.sso.logout_uri",
            ]
        )

    def getRefreshAccessTokenUrl(self):
        return self.constructUrl(
            [
                "services.context.mgmt_api.host",
                "services.context.mgmt_api.sso.refresh_access_token_uri",
            ]
        )

    def getTokenPublicKeyUrl(self):
        return self.constructUrl(
            [
                "services.context.mgmt_api.host",
                "services.context.mgmt_api.sso.public_key_uri",
            ]
        )

    # @cache("kfsd.token.publickey")
    def tokenPublicKey(self):
        return self.httpGet(self.getTokenPublicKeyUrl(), status.HTTP_200_OK)

    def logout(self):
        return self.httpGet(self.getLogoutUrl(), status.HTTP_200_OK)

    def refreshAccessToken(self, payload):
        return self.httpPost(
            self.getRefreshAccessTokenUrl(), payload, status.HTTP_200_OK
        )
