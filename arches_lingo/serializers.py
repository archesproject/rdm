from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from arches.app.models.models import ResourceInstance, TileModel
from arches.app.models.serializers import ArchesModelSerializer, ArchesTileSerializer
from arches_references.models import ListItem


class SchemeRightsSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "scheme"
        nodegroups = ["rights", "right_statement"]
        fields = "__all__"

    def update(self, instance, validated_data):
        """Repair parenttile until fixed in core."""
        updated = super().update(instance, validated_data)
        if updated.right_statement:
            self.repair_right_statement(updated)
        return updated

    def repair_right_statement(self, instance):
        # Shouldn't need to refresh_from_db() here, but I'll (jtw)
        # look into that later, since this is all just a workaround.
        instance.refresh_from_db()
        instance.right_statement.parenttile = instance.rights
        instance.right_statement.save()
        return instance


### Custom serializers for implementing business logic.
class SchemeLabelTileSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = "scheme"
        root_node = "appellative_status"
        fields = "__all__"

    def validate(self, data):
        data = super().validate(data)
        try:
            PREF_LABEL = ListItem.objects.get(list_item_values__value="prefLabel")
        except ListItem.MultipleObjectsReturned:
            msg = _(
                "Ask your system administrator to deduplicate the prefLabel list items."
            )
            raise ValidationError(msg)

        if data:
            # TODO: reduce nested-fallback awkwardness by returning a dataclass from
            # ReferenceDataType.to_python() and feeding incoming data to it.
            new_label_language = next(
                iter(data.get("appellative_status_ascribed_name_language", None) or []),
                {},
            )
            new_label_type = next(
                iter(data.get("appellative_status_ascribed_relation", None) or []), {}
            )
            current_labels = data["resourceinstance"].appellative_status

            for label in current_labels:
                label_language = next(
                    iter(label.appellative_status_ascribed_name_language or []), {}
                )
                label_type = next(
                    iter(label.appellative_status_ascribed_relation or []), {}
                )
                if (
                    data.get("tileid", None) not in (None, label.tileid)
                    and new_label_type.get("uri", "") == PREF_LABEL.uri
                    and label_type.get("uri", "") == PREF_LABEL.uri
                    and label_language.get("uri", "")
                    == new_label_language.get("uri", "")
                ):
                    msg = _("Only one preferred label per language is permitted.")
                    raise ValidationError(msg)
        return data

class LingoResourceSerializer(ArchesModelSerializer):
    # Link any custom serializers here.
    # TODO: put these back in, need some sort of check/wrapper
    # appellative_status = SchemeLabelTileSerializer(
    #     many=True, required=False, allow_null=True
    # )

    class Meta:
        model = ResourceInstance
        graph_slug = None  # generic
        read_only_graphs = ["group", "person", "textual_work"]  # optional attribute
        nodegroups = "__all__"
        fields = "__all__"


class LingoTileSerializer(ArchesTileSerializer):
    # Link any custom serializers here.
    class Meta:
        model = TileModel
        graph_slug = None  # generic
        root_node = None  # generic
        fields = "__all__"
