from rest_framework import status

from kfsd.apps.core.utils.http.headers.contenttype import ContentType
from kfsd.apps.core.services.base import BaseRequest


class Proxy(BaseRequest):
    def __init__(self, request):
        BaseRequest.__init__(self, request)

    def genHeaders(self, expectedRespCode):
        headers = {
            "X-Resp-Code": str(expectedRespCode),
            "X-APIKey": self.getServicesAPIKey(),
            "Content-Type": ContentType.APPLICATION_JSON,
        }
        for k, v in headers.items():
            self.setHeader(k, v)

        cookies = self.getDjangoRequest().getDjangoReqCookies().getAllCookies()
        self.setCookies(cookies)

    def httpGet(self, url, expStatus):
        self.genHeaders(expStatus)
        return super().httpGet(url, status.HTTP_200_OK)

    def httpPost(self, url, payload, expStatus):
        self.genHeaders(expStatus)
        return super().httpPost(url, payload, status.HTTP_200_OK)

    def httpDel(self, url, expStatus):
        self.genHeaders(expStatus)
        return super().httpDel(url, status.HTTP_200_OK)

    def httpPatch(self, url, payload, expStatus):
        self.genHeaders(expStatus)
        return super().httpPatch(url, payload, status.HTTP_200_OK)
