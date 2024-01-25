from datetime import datetime
import json
import logging
from django.core.exceptions import ValidationError
from django.db import connection
from arches.app.etl_modules.decorators import load_data_async
from arches.app.etl_modules.base_data_editor import BaseBulkEditor
from arches.app.models import models
from arches.app.models.concept import Concept, ConceptValue, CORE_CONCEPTS, get_preflabel_from_valueid
from arches.app.models.models import TileModel
from arches.app.models.resource import Resource
from arches.app.models.tile import Tile
import arches_rdm.tasks as tasks
from arches.app.utils.index_database import index_resources_by_transaction

logger = logging.getLogger(__name__)

SCHEME_MAPPINGS = [
    'name_content',
    'name_type',
    'name_language',
    'identifier_content',
    'identifier_type',
]

class RDMMigrator(BaseBulkEditor):
    def __init__(self, request=None, loadid=None):
        self.request = request if request else None
        self.userid = request.user.id if request else None
        self.moduleid = request.POST.get("module") if request else None
        self.loadid = loadid if loadid else None

    def run_migrate_rdm(self, request):

        concept_schemes = []
        for concept in models.Concept.objects.filter(nodetype='ConceptScheme'):
            concept_schemes.append(Concept().get(id=concept.pk, include=["label"]))

        concepts = []
        for concept in models.Concept.objects.filter(nodetype='Concept'):
            concepts.append(Concept().get(id=concept.pk, include=["label"]))

        breakpoint()


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