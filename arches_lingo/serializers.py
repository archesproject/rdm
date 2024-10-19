from arches.app.models.models import ResourceInstance, TileModel
from arches.app.models.serializers import ArchesModelSerializer, ArchesTileSerializer


class SchemeStatementSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = "scheme"
        root_node = "statement"
        fields = "__all__"


class SchemeSerializer(ArchesModelSerializer):
    # TODO: Reduce duplication with Meta.nodegroups, below?
    statement = SchemeStatementSerializer(many=True, required=False)

    class Meta:
        model = ResourceInstance
        graph_slug = "scheme"
        nodegroups = ["statement"]
        fields = "__all__"


class ConceptStatementSerializer(ArchesTileSerializer):
    class Meta:
        model = TileModel
        graph_slug = "concept"
        root_node = "statement"
        fields = "__all__"


class ConceptSerializer(ArchesModelSerializer):
    statement = ConceptStatementSerializer(many=True, required=False)

    class Meta:
        model = ResourceInstance
        graph_slug = "concept"
        nodegroups = ["statement"]
        fields = "__all__"
