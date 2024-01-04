from rest_framework import status

from kfsd.apps.core.services.base import BaseRequest
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class PermissionApi(BaseRequest):
    def __init__(self, request=None):
        BaseRequest.__init__(self, request)

    def genResourceId(self, resource):
        return "{},{}".format(resource.type, resource.identifier)

    def genUserId(self, user):
        return "{},{}".format(user.getUserModel(), user.getUserId())

    def getGatewayUrl(self):
        return self.constructUrl(
            [
                "services.context.gateway_api.host",
                "services.context.perm_api.base_uri",
            ]
        )

    def getAuthResourceUrl(self, userId, resourceId):
        authResourceUri = self.constructUrl(
            [
                "services.context.perm_api.host",
                "services.context.perm_api.auth_resource_uri",
            ]
        )
        return authResourceUri.format(userId, resourceId)

    def getAllResources(self, userId):
        resourcesUri = self.constructUrl(
            [
                "services.context.perm_api.host",
                "services.context.perm_api.auth_resources_all_uri",
            ]
        )
        return resourcesUri.format(userId)

    def authorize(self, userId, perm, resourceId):
        url = self.getAuthResourceUrl(userId, resourceId)
        payload = {"action": perm}
        return self.httpPost(url, payload, status.HTTP_200_OK)

    def authorized_resources(self, userId, perm, resourceType):
        url = self.getAllResources(userId)
        payload = {
            "action": perm,
            "resource_type": "POLICY_TYPE=Resource,POLICY_NAME={}".format(resourceType),
        }
        return self.httpPost(url, payload, status.HTTP_200_OK)
