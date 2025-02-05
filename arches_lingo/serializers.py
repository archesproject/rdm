from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from arches.app.models.models import ResourceInstance, TileModel
from arches.app.models.serializers import ArchesModelSerializer, ArchesTileSerializer
from arches.app.models.tile import Tile

from arches_references.datatypes.datatypes import ReferenceDataType
from arches_references.models import ListItem


# Generic serializers for Lingo.
class LingoResourceSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = None  # generic
        nodegroups = "__all__"
        fields = "__all__"

    def create(self, validated_data):
        """Repair parenttile until fixed in core."""
        created = super().create(validated_data)
        if created.right_statement:
            self.repair_right_statement(created)
        return created

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
        if not instance.rights:
            instance.rights = Tile.get_blank_tile_from_nodegroup_id(
                instance.right_statement.nodegroup.parentnodegroup_id,
                resourceid=instance.resourceinstanceid,
            )
            instance.rights.save()

        instance.right_statement.parenttile = instance.rights
        instance.right_statement.save()
        return instance


class LingoTileSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = None  # generic
        root_node = None  # generic
        fields = "__all__"

    def validate_appellative_status(self, data):
        try:
            PREF_LABEL = ListItem.objects.get(list_item_values__value="prefLabel")
        except ListItem.MultipleObjectsReturned:
            msg = _(
                "Ask your system administrator to deduplicate the prefLabel list items."
            )
            raise ValidationError(msg)

        if data:
            # TODO: consider having serializer run to_python().
            new_label_languages = ReferenceDataType.to_python(
                data.get("appellative_status_ascribed_name_language")
            )
            if new_label_languages:
                new_label_language = new_label_languages[0]
            else:
                return data
            new_label_types = ReferenceDataType.to_python(
                data.get("appellative_status_ascribed_relation")
            )
            if new_label_types:
                new_label_type = new_label_types[0]
            else:
                return data

            current_labels = data["resourceinstance"].appellative_status or []
            for label in current_labels:
                if label_languages := label.appellative_status_ascribed_name_language:
                    label_language = label_languages[0]
                else:
                    continue
                if label_types := label.appellative_status_ascribed_relation:
                    label_type = label_types[0]
                else:
                    continue
                if (
                    data.get("tileid") != label.tileid
                    and new_label_type.uri == PREF_LABEL.uri
                    and label_type.uri == PREF_LABEL.uri
                    and label_language.uri == new_label_language.uri
                ):
                    msg = _("Only one preferred label per language is permitted.")
                    raise ValidationError(msg)
        return data
