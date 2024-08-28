from django.db import models

from arches_lingo.query_utils import LevenshteinLessEqual


class LabelValueQuerySet(models.QuerySet):

    def fuzzy_search(self, term, max_edit_distance):
        from arches_lingo.models import VwLabelValue

        return (
            VwLabelValue.objects.all()
            .annotate(
                edit_distance=LevenshteinLessEqual(
                    models.F("value"),
                    models.Value(term),
                    models.Value(max_edit_distance),
                    output_field=models.FloatField(),
                )
            )
            .filter(edit_distance__lte=max_edit_distance)
            .order_by("edit_distance")
        )
