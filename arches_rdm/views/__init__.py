from collections import defaultdict

from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import CharField, F, OuterRef, Value
from django.db.models.expressions import CombinedExpression, Func
from django.utils.decorators import method_decorator
from django.views.generic import View

from arches.app.models.models import ResourceInstance, TileModel
from arches.app.utils.decorators import group_required

from arches.app.utils.response import JSONResponse

TOP_CONCEPT_OF_NODE_AND_NODEGROUP = "bf73e5b9-4888-11ee-8a8d-11afefc4bff7"
TOP_CONCEPT_OF_LOOKUP = f"data__{TOP_CONCEPT_OF_NODE_AND_NODEGROUP}"

BROADER_NODE_AND_NODEGROUP = "bf73e5f5-4888-11ee-8a8d-11afefc4bff7"
BROADER_LOOKUP = f"data__{BROADER_NODE_AND_NODEGROUP}"

CONCEPT_LABEL_NODEGROUP = "bf73e616-4888-11ee-8a8d-11afefc4bff7"
CONCEPT_LABEL_NODE = "bf73e695-4888-11ee-8a8d-11afefc4bff7"
CONCEPT_LABEL_LOOKUP = f"data__{CONCEPT_LABEL_NODE}"

SCHEME_LABEL_NODE_AND_NODEGROUP = "749a27cf-423c-11ee-8a8d-11afefc4bff7"
SCHEME_LABEL_NODE = "749a27d5-423c-11ee-8a8d-11afefc4bff7"
SCHEME_LABEL_LOOKUP = f"data__{SCHEME_LABEL_NODE}"

CONCEPTS_GRAPH_ID = "bf73e576-4888-11ee-8a8d-11afefc4bff7"
SCHEMES_GRAPH_ID = "56788995-423b-11ee-8a8d-11afefc4bff7"


class JsonArrayElements(Func):
    contains_subquery = True
    function = "JSONB_ARRAY_ELEMENTS"


@method_decorator(
    group_required("RDM Administrator", raise_exception=True), name="dispatch"
)
class ConceptTreeView(View):
    def __init__(self):
        self.schemes = ResourceInstance.objects.none()
        self.top_concepts = defaultdict(set)
        self.narrower_concepts = defaultdict(set)  # str: str
        self.labels = defaultdict(set)

    @staticmethod
    def resources_from_tiles(lookup_expression: str):
        return CombinedExpression(
            JsonArrayElements(F(lookup_expression)),
            "->>",
            Value("resourceId"),
            output_field=CharField(),
        )

    @staticmethod
    def labels_subquery(label_lookup):
        if label_lookup == SCHEME_LABEL_LOOKUP:
            # Annotating a ResourceInstance
            outer = OuterRef("resourceinstanceid")
            nodegroup_id = SCHEME_LABEL_NODE_AND_NODEGROUP
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
