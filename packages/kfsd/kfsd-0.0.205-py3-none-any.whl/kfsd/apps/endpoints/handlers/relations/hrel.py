from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from kfsd.apps.endpoints.serializers.relations.hrel import (
    HRelModelSerializer,
    HRelViewModelSerializer,
)
from kfsd.apps.endpoints.handlers.relations.base import BaseHRelHandler
from kfsd.apps.models.tables.relations.hrel import HRel


def gen_hrel_handler(instance):
    handler = HRelHandler(instance.identifier, False)
    qsData = HRelModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=HRel)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=HRel)
def process_post_del(sender, instance, **kwargs):
    pass


class HRelHandler(BaseHRelHandler):
    def __init__(self, hrelIdentifier, isDBFetch):
        BaseHRelHandler.__init__(
            self,
            serializer=HRelModelSerializer,
            viewSerializer=HRelViewModelSerializer,
            modelClass=HRel,
            identifier=hrelIdentifier,
            isDBFetch=isDBFetch,
        )
