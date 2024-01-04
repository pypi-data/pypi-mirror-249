import jwt
from rest_framework import status
from kfsd.apps.core.exceptions.api import KubefacetsAPIException


class JwtHandler:
    def generateToken(self, algo, privateKey, payload):
        return jwt.encode(payload, privateKey, algorithm=algo)

    def decodeToken(self, algo, publicKey, token):
        try:
            return jwt.decode(token, publicKey, algorithms=[algo])
        except jwt.exceptions.InvalidSignatureError as e:
            raise KubefacetsAPIException(
                "Invalid signature - Signature verification failed",
                "bad_request",
                status.HTTP_400_BAD_REQUEST,
                e.__str__(),
            )
        except jwt.exceptions.DecodeError as e:
            raise KubefacetsAPIException(
                "Invalid signature - Signature verification failed",
                "bad_request",
                status.HTTP_400_BAD_REQUEST,
                e.__str__(),
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            raise KubefacetsAPIException(
                "Token expired",
                "token_expired",
                status.HTTP_401_UNAUTHORIZED,
                e.__str__(),
            )
