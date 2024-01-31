from datetime import datetime
import logging
from django.core.exceptions import ValidationError
from django.db import connection
from arches.app.etl_modules.decorators import load_data_async
from arches.app.etl_modules.base_import_module import BaseImportModule, FileValidationError
from arches.app.models import models
from arches.app.models.concept import Concept, ConceptValue, CORE_CONCEPTS, get_preflabel_from_valueid
from arches.app.models.models import GraphModel, TileModel
import arches_rdm.tasks as tasks
from arches.app.utils.index_database import index_resources_by_transaction

logger = logging.getLogger(__name__)

#### Constants ####
CONCEPTS_GRAPH_ID = "bf73e576-4888-11ee-8a8d-11afefc4bff7"
SCHEMES_GRAPH_ID = "56788995-423b-11ee-8a8d-11afefc4bff7"


class RDMMigrator(BaseImportModule):
    def __init__(self, request=None, loadid=None):
        self.request = request if request else None
        self.userid = request.user.id if request else None
        self.moduleid = request.POST.get("module") if request else None
        self.loadid = loadid if loadid else None
    
    # def create_tile_value(self, tile_values, data_node_lookup, )

    def run_migrate_rdm(self, request):

        nodegroup_lookup, nodes = self.get_graph_tree(SCHEMES_GRAPH_ID)
        node_lookup = self.get_node_lookup(nodes)

        schemes = []
        for concept in models.Concept.objects.filter(nodetype="ConceptScheme"):
            scheme = {}

            concept_value = Concept().get(id=concept.pk, include=["label"])
            for value in concept_value.values:
                scheme["legacyid"] = value.conceptid
                scheme["resourceinstanceid"] = value.id # use old valueid as new resourceinstanceid

                scheme["tile_data"] = []
                name = {}
                name["name_content"] = value.value
                name["name_language"] = value.language
                name["name_type"] = value.type
                scheme["tile_data"].append({'name': name})
            
            schemes.append(scheme)

        tiles = []

        for scheme in schemes:
            for mock_tile in scheme["tile_data"]:
                tile_data = {}
                for nodegroup_id in nodegroup_lookup.keys():
                    nodegroup_alias = nodegroup_lookup[nodegroup_id]["alias"]
                    try:
                        if mock_tile[nodegroup_alias]:
                            tile_data[nodegroup_id] = {}
                            for mock_node in list(mock_tile[nodegroup_alias]):
                                nodeid = node_lookup[mock_node]['nodeid']
                                tile_data[nodegroup_id][nodeid] = mock_tile[nodegroup_alias][mock_node]
                    except KeyError:
                        pass

        # concepts = []
        # for concept in models.Concept.objects.filter(nodetype='Concept'):
        #     concepts.append(Concept().get(id=concept.pk, include=["label"]))



        # operation = 'insert'
        # if user_tileid:
        #     if nodegroup_cardinality == "n":
        #         operation = "update" # db will "insert" if tileid does not exist
        #     elif nodegroup_cardinality == "1":
        #         if TileModel.objects.filter(pk=tileid).exists():
        #             operation = "update"
        # cursor.execute("""
        #     INSERT INTO load_staging (
        #         nodegroupid,
        #         legacyid,
        #         resourceid,
        #         tileid,
        #         parenttileid,
        #         value,
        #         loadid,
        #         nodegroup_depth,
        #         source_description,
        #         passes_validation,
        #         operation
        #     ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        #     (
        #         row_details["nodegroup_id"],
        #         legacyid,
        #         resourceid,
        #         tileid,
        #         parenttileid,
        #         tile_value_json,
        #         self.loadid,
        #         nodegroup_depth,
        #         "worksheet:{0}, row:{1}".format(worksheet.title, row[0].row),  # source_description
        #         passes_validation,
        #         operation,
        #     ),
        # )
            
        

    @load_data_async
    def run_load_task_async(self, request):
        self.loadid = request.POST.get("load_id")
        # graph_id = request.POST.get("graph_id", None)
        # graph_name = request.POST.get("graph_name", None)
        # resource_ids = request.POST.get("resource_ids", None)

        migrate_task = tasks.migrate_rdm.apply_async(
            (self.userid, self.loadid),
            # (self.userid, self.loadid, graph_id, graph_name, resource_ids),
        )

        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE load_event SET taskid = %s WHERE loadid = %s""",
                (migrate_task.task_id, self.loadid),
            )