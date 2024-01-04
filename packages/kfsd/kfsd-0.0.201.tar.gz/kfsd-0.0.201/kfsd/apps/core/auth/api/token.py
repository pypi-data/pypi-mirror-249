from rest_framework import status

from kfsd.apps.core.services.token import TokenApi
from kfsd.apps.core.services.permission import PermissionApi
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.auth.jwt import JwtHandler
from kfsd.apps.core.exceptions.api import KubefacetsAPIException


logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class TokenAuth(TokenApi, PermissionApi):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"

    def __init__(self, request=None):
        TokenApi.__init__(self, request)
        PermissionApi.__init__(self, request)
        self.__cookies = []

    def getTokenUserInfo(self):
        cookies = self.getDjangoRequest().getDjangoReqCookies().getAllCookies()
        accessToken = DictUtils.get(cookies, self.ACCESS_TOKEN)
        refreshToken = DictUtils.get(cookies, self.REFRESH_TOKEN)
        return self.extractUserInfoFromTokens(accessToken, refreshToken)

    def extractUserInfoFromTokens(self, accessToken, refreshToken):
        if not accessToken and not refreshToken:
            return self.unAuthorized(self.genNoTokensError())
        elif accessToken:
            try:
                return self.constructGatewayResp(
                    True,
                    {"user": self.decToken(accessToken), "cookies": self.__cookies},
                )
            except KubefacetsAPIException:
                return self.extractUserInfoFromTokens(None, refreshToken)
        elif refreshToken:
            try:
                refreshAccessTokenResp = self.refreshAccessToken(
                    {"token": refreshToken}
                )
                self.__cookies = DictUtils.get_by_path(
                    refreshAccessTokenResp, "data.cookies"
                )
                userInfo = DictUtils.get_by_path(refreshAccessTokenResp, "data.user")
                return self.constructGatewayResp(
                    True,
                    {"user": userInfo, "cookies": self.__cookies},
                )
            except KubefacetsAPIException as e:
                self.genLogout()
                return self.unAuthorized(self.readExceptionError(e))
        return self.unAuthorized()

    def decToken(self, token):
        tokenPublicKeyResp = self.tokenPublicKey()
        algo = DictUtils.get_by_path(tokenPublicKeyResp, "data.algo")
        publicKey = DictUtils.get_by_path(tokenPublicKeyResp, "data.public")
        return JwtHandler().decodeToken(algo, publicKey, token)

    def unAuthorized(self, e=None):
        error = {}
        if e:
            error = e
            logger.logWebRequestError(
                self.getDjangoRequest().getRequest(),
                error,
                DictUtils.get(error, "type"),
            )
        return self.constructGatewayResp(
            False, {"user": {}, "cookies": self.__cookies}, error
        )

    def genLogout(self):
        logoutResp = self.logout()
        self.__cookies = DictUtils.get_by_path(logoutResp, "data.cookies")

    def genNoTokensError(self):
        return {
            "detail": "no tokens found",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "default_code": "no_tokens",
            "type": "debug",
        }
