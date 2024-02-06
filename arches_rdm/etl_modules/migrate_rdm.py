from datetime import datetime
import json
import logging
import uuid
from django.core.exceptions import ValidationError
from django.db import connection
from arches.app.datatypes.datatypes import DataTypeFactory
from arches.app.etl_modules.decorators import load_data_async
from arches.app.etl_modules.base_import_module import BaseImportModule, FileValidationError
from arches.app.models import models
from arches.app.models.concept import Concept, ConceptValue, CORE_CONCEPTS, get_preflabel_from_valueid
from arches.app.models.models import GraphModel, TileModel
from arches.app.utils.betterJSONSerializer import JSONSerializer
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
        self.loadid = request.POST.get("loadid") if request else loadid
        self.datatype_factory = DataTypeFactory()
    
    def etl_schemes(self, cursor, nodegroup_lookup, node_lookup):
        schemes = []
        for concept in models.Concept.objects.filter(nodetype="ConceptScheme"):
            concept_value = Concept().get(id=concept.pk, include=["label"])

            for value in concept_value.values:
                scheme = {"type": "Scheme"}
                scheme["legacyid"] = value.conceptid
                scheme["resourceinstanceid"] = value.id # use old valueid as new resourceinstanceid

                scheme["tile_data"] = []
                name = {}
                name["name_content"] = value.value
                # name["name_language"] = value.language
                # name["name_type"] = value.type
                scheme["tile_data"].append({"name": name})

                self.populate_staging_table(cursor, scheme, nodegroup_lookup, node_lookup)

    def populate_staging_table(self, cursor, concept_to_load, nodegroup_lookup, node_lookup):
        for mock_tile in concept_to_load["tile_data"]:
            nodegroup_alias = next(iter(mock_tile.keys()), None)
            nodegroup_id = node_lookup[nodegroup_alias]["nodeid"]
            nodegroup_depth = nodegroup_lookup[nodegroup_id]["depth"]
            tile_id = uuid.uuid4()
            parent_tile_id = None
            tile_value_json, passes_validation = self.create_tile_value(cursor, mock_tile, nodegroup_alias, nodegroup_lookup, node_lookup)
            operation = "insert"

            cursor.execute("""
                INSERT INTO load_staging (
                    nodegroupid,
                    legacyid,
                    resourceid,
                    tileid,
                    parenttileid,
                    value,
                    loadid,
                    nodegroup_depth,
                    source_description,
                    passes_validation,
                    operation
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    nodegroup_id,
                    concept_to_load["legacyid"],
                    concept_to_load["resourceinstanceid"],
                    tile_id,
                    parent_tile_id,
                    tile_value_json,
                    self.loadid,
                    nodegroup_depth,
                    "{0}: {1}".format(concept_to_load["type"], nodegroup_alias),  # source_description
                    passes_validation,
                    operation,
                ),
            )
        cursor.execute("""CALL __arches_check_tile_cardinality_violation_for_load(%s)""", [self.loadid])
        cursor.execute(
            """
            INSERT INTO load_errors (type, source, error, loadid, nodegroupid)
            SELECT 'tile', source_description, error_message, loadid, nodegroupid
            FROM load_staging
            WHERE loadid = %s AND passes_validation = false AND error_message IS NOT null
            """,
            [self.loadid],
        )

    def create_tile_value(self, cursor, mock_tile, nodegroup_alias, nodegroup_lookup, node_lookup):
        tile_value = {}
        tile_valid = True
        for node_alias in mock_tile[nodegroup_alias].keys():
            try:
                nodeid = node_lookup[node_alias]["nodeid"]
                node_details = node_lookup[node_alias]
                datatype = node_details["datatype"]
                datatype_instance = self.datatype_factory.get_instance(datatype)
                source_value = mock_tile[nodegroup_alias][node_alias]
                config = node_details["config"]
                config["loadid"] = self.loadid
                config["nodeid"] = nodeid
                
                value, validation_errors = self.prepare_data_for_loading(datatype_instance, source_value, config)
                valid = True if len(validation_errors) == 0 else False
                if not valid:
                    tile_valid = False
                error_message = ""
                for error in validation_errors:
                    error_message = "{0}|{1}".format(error_message, error["message"]) if error_message != "" else error["message"]
                    cursor.execute(
                        """INSERT INTO load_errors (type, value, source, error, message, datatype, loadid, nodeid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                        ("node", source_value, "", error["title"], error["message"], datatype, self.loadid, nodeid),
                    )
                
                tile_value[nodeid] = {"value": value, "valid": valid, "source": source_value, "notes": error_message, "datatype": datatype}
            except KeyError:
                pass 

        tile_value_json = JSONSerializer().serialize(tile_value)
        return tile_value_json, tile_valid

    def start(self, request):
        load_details = {"operation": "RDM Migration"}
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO load_event (loadid, complete, status, etl_module_id, load_details, load_start_time, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (self.loadid, False, "running", self.moduleid, json.dumps(load_details), datetime.now(), self.userid),
        )
        message = "load event created"
        
        nodegroup_lookup, nodes = self.get_graph_tree(SCHEMES_GRAPH_ID)
        node_lookup = self.get_node_lookup(nodes)

        self.etl_schemes(cursor, nodegroup_lookup, node_lookup)
        
        return {"success": True, "data": message}


        # concepts = []
        # for concept in models.Concept.objects.filter(nodetype='Concept'):
        #     concepts.append(Concept().get(id=concept.pk, include=["label"])) 
        

    @load_data_async
    def run_load_task_async(self, request):
        self.loadid = request.POST.get("loadid")
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