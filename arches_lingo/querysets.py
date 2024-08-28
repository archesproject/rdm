from django.db import models

from arches_lingo.query_utils import LevenshteinLessEqual


class LabelValueQuerySet(models.QuerySet):

    def fuzzy_search(self, term, max_edit_distance):
        from arches_lingo.models import VwLabelValue

        fuzzy_matches = VwLabelValue.objects.annotate(
            edit_distance=LevenshteinLessEqual(
                models.F("value"),
                models.Value(term),
                models.Value(max_edit_distance),
                output_field=models.FloatField(),
            )
        ).filter(edit_distance__lte=max_edit_distance)
        substring_matches = VwLabelValue.objects.filter(value__icontains=term).annotate(
            edit_distance=models.Value(0)
        )
        matches = substring_matches | fuzzy_matches

        return matches.order_by("edit_distance", "concept_id")
