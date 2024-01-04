import requests
import json

from kfsd.apps.core.utils.http.headers.contenttype import ContentType
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.http.base import HTTP
from kfsd.apps.core.utils.http.headers.base import Headers
from kfsd.apps.core.utils.http.django.request import DjangoRequest
from kfsd.apps.core.exceptions.api import KubefacetsAPIException


class BaseRequest(Headers, HTTP):
    def __init__(self, request):
        self.__request = DjangoRequest(request)
        Headers.__init__(self)
        HTTP.__init__(self)

    def genHeaders(self):
        headers = {
            "X-APIKey": self.getServicesAPIKey(),
            "Content-Type": ContentType.APPLICATION_JSON,
        }
        for k, v in headers.items():
            self.setHeader(k, v)

        cookies = self.getDjangoRequest().getDjangoReqCookies().getAllCookies()
        self.setCookies(cookies)

    def getDjangoRequest(self):
        return self.__request

    def getServicesAPIKey(self):
        return self.getDjangoRequest().findConfigs(["services.api_key"])[0]

    def readExceptionError(self, e):
        return {
            "detail": e.detail,
            "status_code": e.status_code,
            "default_code": e.default_code,
            "type": "error",
        }

    def isGatewayFormatResp(self):
        try:
            return DictUtils.key_exists_multi(
                self.getJsonResponse(), ["status", "data", "error"]
            )
        except Exception:
            return False

    def setSuccessResponse(self, resp):
        response = requests.models.Response()
        response.status_code = 200
        response.headers = {"Content-Type": ContentType.APPLICATION_JSON}
        successResp = self.constructGatewayResp(True, resp, {})
        response._content = bytes(json.dumps(successResp), "utf-8")
        self.setResponse(response)

    def isHTTPRequestSuccessfull(self):
        return DictUtils.get(self.getJsonResponse(), "status")

    def constructGatewayResp(self, status, data, errors={}):
        return {
            "status": status,
            "data": data,
            "error": errors,
        }

    def setErrorResponse(self, e):
        response = requests.models.Response()
        response.status_code = 200
        response.headers = {"Content-Type": ContentType.APPLICATION_JSON}
        errorResp = self.constructGatewayResp(False, {}, self.readExceptionError(e))
        response._content = bytes(json.dumps(errorResp), "utf-8")
        self.setResponse(response)

    def constructUrl(self, configPaths):
        uris = self.getDjangoRequest().findConfigs(configPaths)
        return self.formatUrl(uris)

    def httpGet(self, getUrl, expStatus):
        try:
            self.genHeaders()
            self.get(getUrl, expStatus, headers=self.getReqHeaders())
            if not self.isGatewayFormatResp():
                self.setSuccessResponse(self.getJsonResponse())
                return self.getJsonResponse()
            return self.getJsonResponse()
        except KubefacetsAPIException as e:
            self.setErrorResponse(e)
            return self.getJsonResponse()

    def httpPost(self, url, payload, expStatus):
        try:
            self.genHeaders()
            self.post(url, expStatus, json=payload, headers=self.getReqHeaders())
            if not self.isGatewayFormatResp():
                self.setSuccessResponse(self.getJsonResponse())
                return self.getJsonResponse()
            return self.getJsonResponse()
        except KubefacetsAPIException as e:
            self.setErrorResponse(e)
            return self.getJsonResponse()

    def httpDel(self, url, expStatus):
        try:
            self.genHeaders()
            self.delete(url, expStatus, headers=self.getReqHeaders())
            if not self.isGatewayFormatResp():
                self.setSuccessResponse(self.getJsonResponse())
                return self.getJsonResponse()
            return self.getJsonResponse()
        except KubefacetsAPIException as e:
            self.setErrorResponse(e)
            return self.getJsonResponse()

    def httpPatch(self, url, payload, expStatus):
        try:
            self.genHeaders()
            self.patch(url, expStatus, json=payload, headers=self.getReqHeaders())
            if not self.isGatewayFormatResp():
                self.setSuccessResponse(self.getJsonResponse())
                return self.getJsonResponse()
            return self.getJsonResponse()
        except KubefacetsAPIException as e:
            self.setErrorResponse(e)
            return self.getJsonResponse()

    def isAuthEnabled(self):
        isAuth = self.getDjangoRequest().findConfigs(
            ["services.features_enabled.auth"]
        )[0]
        return isAuth if isAuth else False
