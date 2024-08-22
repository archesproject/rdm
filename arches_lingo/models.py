from django.db import models

from arches.app.models.models import ResourceInstance


class VwLabelValue(models.Model):
    concept = models.ForeignKey(
        ResourceInstance,
        related_name="label_values",
        on_delete=models.DO_NOTHING,
        db_column="conceptid",
    )
    value = models.CharField(db_column="value")

    class Meta:
        managed = False
        db_table = f"arches_lingo__vw_label_values"
