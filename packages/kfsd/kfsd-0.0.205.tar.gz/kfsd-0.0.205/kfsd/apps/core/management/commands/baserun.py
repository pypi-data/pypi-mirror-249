from django.core.management.base import BaseCommand
from django.apps import apps
from pathlib import Path

from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.system import System
from kfsd.apps.core.utils.file import FileUtils
import os

from kfsd.apps.endpoints.serializers.general.data import DataModelSerializer
from kfsd.apps.endpoints.serializers.general.file import FileModelSerializer
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
from kfsd.apps.endpoints.serializers.relations.relation import RelationModelSerializer
from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    HierarchyInitModelSerializer,
)

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Command(BaseCommand):
    help = "Run Setup"
    working_dir = None
    settings = None
    env = None
    type = None
    utils_version = None
    config = {}

    def __init__(self):
        self.config = self.getConfig()
        self.setWorkingDir()

    def getConfig(self):
        return {}

    def getBaseSerializers(self):
        return {
            "models.data": DataModelSerializer,
            "models.file": FileModelSerializer,
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
            "models.relation": RelationModelSerializer,
            "models.hierarchyinit": HierarchyInitModelSerializer,
        }

    def getAppSerializers(self):
        return {}

    def getSerializer(self, model):
        mapping = DictUtils.merge(
            dict1=self.getBaseSerializers(), dict2=self.getAppSerializers()
        )
        if model in mapping:
            return mapping[model]
        else:
            logger.error("Serializer mapping for model str: {} not found".format(model))

    def setWorkingDir(self):
        system = System()
        system.cmdExec("pwd", True)
        self.working_dir = system.getCmdExecOutput()

    def add_arguments(self, parser):
        parser.add_argument(
            "--env",
            type=str,
            help="Fixture Environment - kubefacets, development, test",
        ),
        parser.add_argument(
            "--type",
            type=str,
            help="setup or data",
        )
        parser.add_argument(
            "--utils_version",
            type=str,
            help="setup or data",
        )

    def rm_db(self):
        FileUtils.rm_file("db.sqlite3")

    def update_req_file(self):
        filePath = "requirements.txt"
        requirements = FileUtils.read(filePath)
        requirements = [req for req in requirements if not req.startswith("kfsd")]
        requirements.append("kfsd=={}".format(self.utils_version))
        requirementsStr = "\n".join(requirements)
        FileUtils.write(filePath, requirementsStr)

    def update_utils_pkg(self):
        if self.utils_version:
            self.update_req_file()
            cmds = ["pip install -r requirements.txt"]
            System().cmdsExec(cmds, False)

    def clean_db(self):
        system = System()
        self.rm_db()
        if self.utils_version:
            migrationsDir = FileUtils.construct_path(
                self.working_dir, "kubefacets/apps/backend/migrations"
            )
            FileUtils.rm_dir(migrationsDir)
            FileUtils.create_dir(migrationsDir)

            kfsdMigrationsDir = FileUtils.construct_path(
                self.working_dir,
                "py_env/lib/python3.10/site-packages/kfsd/apps/models/migrations",
            )
            FileUtils.rm_dir(kfsdMigrationsDir)
            FileUtils.create_dir(kfsdMigrationsDir)
            cmds = [
                "touch {}/__init__.py".format(migrationsDir),
                "touch {}/__init__.py".format(kfsdMigrationsDir),
            ]
            system.cmdsExec(cmds, False)
        else:
            migrationsDir = FileUtils.construct_path(
                self.working_dir, "kfsd/apps/models/migrations"
            )
            FileUtils.rm_dir(migrationsDir)
            FileUtils.create_dir(migrationsDir)
            cmd = "touch {}/__init__.py".format(migrationsDir)
            system.cmdExec(cmd, False)

    def run(self):
        fileFormat = ""
        config = self.config[self.env]
        envs = config["env"]

        system = System()

        for k, v in envs.items():
            os.environ[k] = v
            fileFormat += "export {}='{}'\n".format(k, v)

        if self.type == "cleanup":
            fns = config[self.type]
            [fn() for fn in fns]
        elif self.type in ["server", "msmq", "exec"]:
            serverCmd = config[self.type]
            cmd = "{} --settings={}".format(serverCmd, self.settings)
            fileFormat += "{}\n".format(cmd)
            FileUtils.write("{}.sh".format(self.type), fileFormat)
        elif self.type == "migrate":
            cmds = config[self.type]
            for cmd in cmds:
                system.cmdExec("{} --settings={}".format(cmd, self.settings), False)
        elif self.type == "raw_fixtures":
            fixtures = config[self.type]
            cmds = [
                "python manage.py loaddata {} --settings={}".format(
                    fixture, self.settings
                )
                for fixture in fixtures
            ]

            for cmd in cmds:
                system.cmdExec(cmd, False)
        else:
            fixtures = config[self.type]
            for fixture in fixtures:
                self.load_fixture(fixture)

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

    def handle(self, *args, **options):
        self.env = DictUtils.get(options, "env")
        self.type = DictUtils.get(options, "type")
        self.settings = DictUtils.get(options, "settings")
        self.utils_version = DictUtils.get(options, "utils_version", None)
        logger.info("Running setup for env: {}, type: {}".format(self.env, self.type))
        self.run()
