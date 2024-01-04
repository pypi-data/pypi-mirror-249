from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import MAX_LENGTH


class HRel(BaseModel):
    type = models.CharField(max_length=MAX_LENGTH)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="rel_children",
    )
    created_by = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="rel_owned",
    )
    is_public = models.BooleanField(default=False)

    class Meta:
        app_label = "models"
        verbose_name = "HRel"
        verbose_name_plural = "HRels"
