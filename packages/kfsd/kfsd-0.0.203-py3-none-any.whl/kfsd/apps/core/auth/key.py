from kfsd.apps.core.auth.base import BaseUser
from kfsd.apps.core.auth.api.key import APIKeyAuth


class APIKeyUser(BaseUser, APIKeyAuth):
    def __init__(self, request):
        BaseUser.__init__(self)
        APIKeyAuth.__init__(self, request=request)
        self.setUserInfo(self.getApiKeyUserInfo()) if self.isAuthEnabled() else {}
