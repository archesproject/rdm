from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from arches.app.models.models import ResourceInstance, TileModel
from arches.app.models.serializers import ArchesModelSerializer, ArchesTileSerializer

from arches_controlled_lists.datatypes.datatypes import ReferenceDataType
from arches_controlled_lists.models import ListItem


# Generic serializers for Lingo.
class LingoResourceSerializer(ArchesModelSerializer):
    class Meta:
        model = ResourceInstance
        graph_slug = None  # generic
        nodegroups = "__all__"
        fields = "__all__"


class LingoTileSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = None
        root_node = None
        fields = "__all__"

    def validate_appellative_status(self, data):
        if data:
            # TODO: consider having serializer run to_python().
            if new_label_languages := ReferenceDataType().to_python(
                data.get("appellative_status_ascribed_name_language")
            ):
                new_label_lang = new_label_languages[0]
            if new_label_types := ReferenceDataType().to_python(
                data.get("appellative_status_ascribed_relation")
            ):
                new_label_type = new_label_types[0]

            if new_label_lang and new_label_type:
                self._check_pref_label_uniqueness(data, new_label_lang, new_label_type)

        return data

    @staticmethod
    def _check_pref_label_uniqueness(data, new_label_language, new_label_type):
        try:
            PREF_LABEL = ListItem.objects.get(list_item_values__value="prefLabel")
        except ListItem.MultipleObjectsReturned:
            msg = _(
                "Ask your system administrator to deduplicate the prefLabel list items."
            )
            raise ValidationError(msg)

        for label in data["resourceinstance"].appellative_status or []:
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
