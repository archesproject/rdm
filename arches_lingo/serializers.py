from rest_framework.exceptions import ValidationError

from arches_references.models import ListItem

from arches.app.models.models import ResourceInstance, TileModel
from arches.app.models.serializers import ArchesModelSerializer, ArchesTileSerializer


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
        graph_slug = self.Meta.graph_slug
        PREF_LABEL_LIST_ITEM = ListItem.objects.get(list_item_values__value="prefLabel")

        if data:
            new_label_language = data["appellative_status_ascribed_name_language"][0]
            new_label_type = data["appellative_status_ascribed_relation"][0]

            resource_instance_id = self.instance.resourceinstance.pk
            resource_instance = self.instance.resourceinstance.__class__.as_model(
                graph_slug, resource_ids=[resource_instance_id]
            ).get(pk=resource_instance_id)
            current_labels = resource_instance.appellative_status
            for label in current_labels:
                if (
                    data["tileid"] != label.tileid
                    and new_label_type["uri"] == PREF_LABEL_LIST_ITEM.uri
                    and label.appellative_status_ascribed_relation[0]["uri"]
                    == PREF_LABEL_LIST_ITEM.uri
                    and label.appellative_status_ascribed_name_language[0]["uri"]
                    == new_label_language["uri"]
                ):
                    raise ValidationError(
                        "A preferred label with the same language already exists for this scheme."
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
