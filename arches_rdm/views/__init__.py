from collections import defaultdict

from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import CharField, F, OuterRef, Value
from django.db.models.expressions import CombinedExpression, Func
from django.utils.decorators import method_decorator
from django.views.generic import View

from arches.app.models.models import ResourceInstance, TileModel
from arches.app.utils.decorators import group_required

from arches.app.utils.response import JSONResponse

from arches_rdm.const import (
    SCHEMES_GRAPH_ID,
    TOP_CONCEPT_OF_NODE_AND_NODEGROUP,
    BROADER_NODE_AND_NODEGROUP,
    CONCEPT_LABEL_NODEGROUP,
    CONCEPT_LABEL_NODE,
    SCHEME_LABEL_NODEGROUP,
    SCHEME_LABEL_NODE,
)

TOP_CONCEPT_OF_LOOKUP = f"data__{TOP_CONCEPT_OF_NODE_AND_NODEGROUP}"
BROADER_LOOKUP = f"data__{BROADER_NODE_AND_NODEGROUP}"
CONCEPT_LABEL_LOOKUP = f"data__{CONCEPT_LABEL_NODE}"
SCHEME_LABEL_LOOKUP = f"data__{SCHEME_LABEL_NODE}"


class JsonbArrayElements(Func):
    """https://forum.djangoproject.com/t/django-4-2-behavior-change-when-using-arrayagg-on-unnested-arrayfield-postgresql-specific/21547/5"""
    contains_subquery = True
    function = "JSONB_ARRAY_ELEMENTS"


@method_decorator(
    group_required("RDM Administrator", raise_exception=True), name="dispatch"
)
class ConceptTreeView(View):
    def __init__(self):
        self.schemes = ResourceInstance.objects.none()
        # key=scheme resourceid (str) val=set of concept resourceids (str)
        self.top_concepts: dict[str: set[str]] = defaultdict(set)
        # key=concept resourceid (str) val=set of concept resourceids (str)
        self.narrower_concepts: dict[str: set[str]] = defaultdict(set)
        # key=resourceid (str) val=list of label dicts
        self.labels: dict[str: list[dict]] = defaultdict(set)

    @staticmethod
    def resources_from_tiles(lookup_expression: str):
        return CombinedExpression(
            JsonbArrayElements(F(lookup_expression)),
            "->>",
            Value("resourceId"),
            output_field=CharField(),
        )

    @staticmethod
    def labels_subquery(label_lookup):
        if label_lookup == SCHEME_LABEL_LOOKUP:
            # Annotating a ResourceInstance
            outer = OuterRef("resourceinstanceid")
            nodegroup_id = SCHEME_LABEL_NODEGROUP
        else:
            # Annotating a Tile
            outer = OuterRef("resourceinstance_id")
            nodegroup_id = CONCEPT_LABEL_NODEGROUP

        return ArraySubquery(
            TileModel.objects.filter(
                resourceinstance_id=outer, nodegroup_id=nodegroup_id
            )
            .values(label_lookup)
        )

    def top_concepts_map(self):
        top_concept_of_tiles = (
            TileModel.objects.filter(nodegroup_id=TOP_CONCEPT_OF_NODE_AND_NODEGROUP)
            .annotate(top_concept_of=self.resources_from_tiles(TOP_CONCEPT_OF_LOOKUP))
            .annotate(labels=self.labels_subquery(CONCEPT_LABEL_LOOKUP))
            .values("resourceinstance_id", "top_concept_of", "labels")
        )
        for tile in top_concept_of_tiles:
            resource_id: str = str(tile["resourceinstance_id"])
            self.top_concepts[tile["top_concept_of"]].add(resource_id)
            self.labels[resource_id] = tile["labels"]

    def narrower_concepts_map(self):
        broader_concept_tiles = (
            TileModel.objects.filter(nodegroup_id=BROADER_NODE_AND_NODEGROUP)
            .annotate(broader_concept=self.resources_from_tiles(BROADER_LOOKUP))
            .annotate(labels=self.labels_subquery(CONCEPT_LABEL_LOOKUP))
            .values("resourceinstance_id", "broader_concept", "labels")
        )
        for tile in broader_concept_tiles:
            resource_id: str = str(tile["resourceinstance_id"])
            self.narrower_concepts[tile["broader_concept"]].add(resource_id)
            self.labels[resource_id] = tile["labels"]

    def serialize_scheme(self, scheme: ResourceInstance):
        scheme_id: str = str(scheme.pk)
        return {
            "resourceinstance_id": scheme_id,
            "labels": [self.serialize_label(label) for label in scheme.labels],
            "top_concepts": [
                self.serialize_concept(concept_id)
                for concept_id in self.top_concepts[scheme_id]
            ],
        }

    def serialize_concept(self, conceptid: str):
        return {
            "resourceinstance_id": conceptid,
            "labels": [self.serialize_label(label) for label in self.labels[conceptid]],
            "narrower": [
                self.serialize_concept(conceptid)
                for conceptid in self.narrower_concepts[conceptid]
            ],
        }

    def serialize_label(self, label: dict):
        for language, inner_dict in label.items():
            return {
                "valuetype": "prefLabel",  # todo: get real
                "language": language,
                "value": inner_dict["value"],
            }

    def get(self, request):
        self.top_concepts_map()
        self.narrower_concepts_map()

        self.schemes = ResourceInstance.objects.filter(
            graph_id=SCHEMES_GRAPH_ID
        ).annotate(labels=self.labels_subquery(SCHEME_LABEL_LOOKUP))

        data = {
            "schemes": [self.serialize_scheme(scheme) for scheme in self.schemes],
        }
        # Todo: filter by nodegroup permissions
        return JSONResponse(data)
