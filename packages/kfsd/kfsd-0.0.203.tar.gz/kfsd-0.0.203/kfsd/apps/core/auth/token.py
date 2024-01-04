from kfsd.apps.core.auth.base import BaseUser
from kfsd.apps.core.auth.api.token import TokenAuth
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class TokenUser(BaseUser, TokenAuth):
    def __init__(self, request):
        BaseUser.__init__(self)
        TokenAuth.__init__(self, request=request)
        tokenUserInfo = self.getTokenUserInfo() if self.isAuthEnabled() else {}
        self.setUserInfo(tokenUserInfo)

    def getUserCookies(self):
        userInfo = self.getUserInfo()
        return DictUtils.get_by_path(userInfo, "data.cookies")

    def getUserId(self):
        userId = DictUtils.get_by_path(self.getUserInfo(), "data.user.identifier")
        if not userId:
            return "USR=anonymous"
        return userId

    def getUserModel(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.type")

    def getEmail(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.email")

    def getFirstName(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.first_name")

    def getMiddleName(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.middle_name")

    def getLastName(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.last_name")

    def getImage(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.image")

    def isEmailVerified(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.is_email_verified")

    def isStaff(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.is_staff")

    def isSuperuser(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.is_superuser")

    def has_perm(self, perm, obj=None):
        resp = self.authorize(self.genUserId(self), perm, self.genResourceId(obj))
        return DictUtils.get(resp, "status")

    def has_perm_all_resources(self, perm, type):
        resp = self.authorized_resources(self.genUserId(self), perm, type)
        return DictUtils.get(resp, "data")

    def has_perms(self, obj=None):
        resp = self.authorize(self.genUserId(self), "*", self.genResourceId(obj))
        return DictUtils.get(resp, "data")
