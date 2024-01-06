from kfsd.apps.core.management.commands.baserun import Command as BaseCommand
from kfsd.apps.core.common.logger import Logger, LogLevel


logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Command(BaseCommand):
    help = "Utils Pkg Setup"
    service_id = "utils_api"

    def getAppSerializers(self):
        return {}

    def getConfig(self):
        return {
            "kubefacets": {
                "env": {
                    "service_id": "{}".format(self.service_id),
                    "env": "dev",
                    "settings_id": "SETTING=Kubefacets",
                    "outbound_policy_id": "POLICY_TYPE=Events,POLICY_NAME=Outbound",
                    "inbound_policy_id": "POLICY_TYPE=Events,POLICY_NAME=Inbound",
                },
                "cleanup": [self.update_utils_pkg, self.clean_db],
                "migrate": [
                    "python manage.py makemigrations",
                    "python manage.py migrate",
                ],
                "setup_fixtures": [
                    "v1/kubefacets/config/settings.json",
                    "v1/kubefacets/events/base.json",
                    "v1/kubefacets/events/events_base_inbound.json",
                    "v1/kubefacets/events/events_base_outbound.json",
                    "v1/kubefacets/events/events_filter_inbound.json",
                    "v1/kubefacets/events/events_filter_outbound.json",
                    "v1/kubefacets/events/events_inbound_clear_inbound_tbl.json",
                    "v1/kubefacets/events/events_inbound_clear_outbound_tbl.json",
                    "v1/kubefacets/events/events_outbound_tbl_upsert.json",
                    "v1/kubefacets/data/test.json",
                ],
                "data_fixtures": [],
                "msmq": "python manage.py basemsmq -s={}".format(self.service_id),
                "server": "python manage.py runserver 8000",
            }
        }
