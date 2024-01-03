from django.apps import apps
from pathlib import Path

from django.test.testcases import TestData

from kfsd.apps.endpoints.serializers.general.data import DataModelSerializer
from kfsd.apps.endpoints.serializers.general.reference import ReferenceModelSerializer
from kfsd.apps.endpoints.serializers.settings.config import ConfigModelSerializer
from kfsd.apps.endpoints.serializers.settings.local import LocalModelSerializer
from kfsd.apps.endpoints.serializers.settings.setting import SettingModelSerializer
from kfsd.apps.endpoints.serializers.rabbitmq.exchange import ExchangeModelSerializer
from kfsd.apps.endpoints.serializers.rabbitmq.route import RouteModelSerializer
from kfsd.apps.endpoints.serializers.rabbitmq.queue import QueueModelSerializer
from kfsd.apps.endpoints.serializers.validations.policy import PolicyModelSerializer
from kfsd.apps.endpoints.serializers.validations.rule import RuleModelSerializer
from kfsd.apps.endpoints.serializers.signals.signal import SignalModelSerializer
from kfsd.apps.endpoints.serializers.requests.endpoint import EndpointModelSerializer
from kfsd.apps.endpoints.serializers.signals.webhook import WebhookModelSerializer
from kfsd.apps.endpoints.serializers.rabbitmq.producer import ProducerModelSerializer
from kfsd.apps.endpoints.serializers.requests.header import HeaderModelSerializer
from kfsd.apps.endpoints.serializers.requests.param import ParamModelSerializer
from kfsd.apps.endpoints.serializers.requests.template import (
    RequestTemplateModelSerializer,
)
from kfsd.apps.endpoints.serializers.settings.remote import RemoteModelSerializer

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.file import FileUtils
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class EndpointsV1TestHandler(EndpointsTestHandler):
    def getBaseSerializers(self):
        return {
            "models.data": DataModelSerializer,
            "models.reference": ReferenceModelSerializer,
            "models.config": ConfigModelSerializer,
            "models.local": LocalModelSerializer,
            "models.setting": SettingModelSerializer,
            "models.exchange": ExchangeModelSerializer,
            "models.route": RouteModelSerializer,
            "models.queue": QueueModelSerializer,
            "models.policy": PolicyModelSerializer,
            "models.rule": RuleModelSerializer,
            "models.signal": SignalModelSerializer,
            "models.endpoint": EndpointModelSerializer,
            "models.webhook": WebhookModelSerializer,
            "models.producer": ProducerModelSerializer,
            "models.header": HeaderModelSerializer,
            "models.param": ParamModelSerializer,
            "models.requesttemplate": RequestTemplateModelSerializer,
            "models.remote": RemoteModelSerializer,
        }

    def getAppSerializers(self):
        return {}

    def getSerializer(self, model):
        mapping = DictUtils.merge(
            dict1=self.getBaseSerializers(),
            dict2=self.getAppSerializers(),
        )
        if model in mapping:
            return mapping[model]
        else:
            logger.error("Serializer mapping for model str: {} not found".format(model))

    def load_fixture(self, fixturePath):
        for app_config in apps.get_app_configs():
            fixture_path = Path(app_config.path, "fixtures", fixturePath)
            if fixture_path.exists():
                self.load_data(fixture_path)

    def load_data(self, fixturePath):
        obj = FileUtils.read_as_json(fixturePath)
        for data in obj:
            model = data["model"]
            fields = data["fields"]
            serializer = self.getSerializer(model)
            serializerObj = serializer(data=fields)
            try:
                if serializerObj.exists():
                    instance = serializerObj.get_instance()
                    serializerObj = serializer(
                        instance=instance, data=fields, partial=True
                    )
                    serializerObj.is_valid(raise_exception=True)
                    serializerObj.save()
                else:
                    serializerObj.is_valid(raise_exception=True)
                    serializerObj.save()
            except Exception as e:
                logger.error("Error: {} occurred for data: {}".format(e, data))
                raise e

    @classmethod
    def setUpClass(cls):
        # super().setUpClass()
        if not cls._databases_support_transactions():
            return
        cls.cls_atomics = cls._enter_atomics()
        pre_attrs = cls.__dict__.copy()
        try:
            cls.setUpTestData()
        except Exception:
            cls._rollback_atomics(cls.cls_atomics)
            raise
        for name, value in cls.__dict__.items():
            if value is not pre_attrs.get(name):
                setattr(cls, name, TestData(name, value))

    def setUp(self):
        for fixture_path in self.fixtures:
            self.load_fixture(fixture_path)

        return super().setUp()
