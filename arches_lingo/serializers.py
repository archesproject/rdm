from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from arches.app.models.models import ResourceInstance, TileModel
from arches.app.models.serializers import ArchesModelSerializer, ArchesTileSerializer
from arches.app.models.tile import Tile
from arches_references.models import ListItem


class SchemeStatementSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = "scheme"
        root_node = "statement"
        fields = "__all__"


class SchemeSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "scheme"
        nodegroups = "__all__"
        fields = "__all__"


class SchemeNamespaceSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "scheme"
        nodegroups = ["namespace"]
        fields = "__all__"


class SchemeCreationSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "scheme"
        nodegroups = ["creation"]
        fields = "__all__"


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
        if instance.rights:
            instance.right_statement.parenttile = instance.rights
        else:
            blank_parent = Tile.get_blank_tile_from_nodegroup_id(
                instance.right_statement.nodegroup.parentnodegroup_id,
                resourceid=instance.resourceinstanceid,
            )
            blank_parent.save()
            instance.right_statement.parenttile = blank_parent

        instance.right_statement.save()
        return instance


class SchemeLabelSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "scheme"
        nodegroups = ["appellative_status"]
        fields = "__all__"


class SchemeLabelTileSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = "scheme"
        root_node = "appellative_status"
        fields = "__all__"

    def validate(self, data):
        data = super().validate(data)
        try:
            PREF_LABEL_LIST_ITEM = ListItem.objects.get(
                list_item_values__value="prefLabel",
            )
        except ListItem.MultipleObjectsReturned:
            raise RuntimeError(
                _(
                    "Ask your system administrator to deduplicate the prefLabel list items."
                )
            )

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
                    and new_label_type.get("uri", "") == PREF_LABEL_LIST_ITEM.uri
                    and label_type.get("uri", "") == PREF_LABEL_LIST_ITEM.uri
                    and label_language.get("uri", "")
                    == new_label_language.get("uri", "")
                ):
                    raise ValidationError(
                        _("Only one preferred label per language is permitted.")
                    )
        return data


class SchemeNoteSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "scheme"
        nodegroups = ["statement"]
        fields = "__all__"


class SchemeNoteTileSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = "scheme"
        root_node = "statement"
        fields = "__all__"


class TextualWorkRdmSystemSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "textual_work"
        nodegroups = "__all__"
        fields = "__all__"


class ConceptStatementSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = "concept"
        root_node = "statement"
        fields = "__all__"


class ConceptSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "concept"
        nodegroups = "__all__"
        fields = "__all__"


class PersonRdmSystemSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "person"
        nodegroups = "__all__"
        fields = "__all__"


class GroupRdmSystemSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = "group"
        nodegroups = "__all__"
        fields = "__all__"
