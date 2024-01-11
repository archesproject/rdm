from datetime import datetime
import json
import logging
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import connection
from django.http import HttpRequest
from django.utils.translation import gettext as _
from arches.app.etl_modules.base_data_editor import BaseBulkEditor
from arches.app.etl_modules.decorators import load_data_async
from arches.app.models.models import TileModel
from arches.app.models.resource import Resource
from arches.app.models.system_settings import settings
from arches.app.models.tile import Tile
import arches.app.tasks as tasks
from arches.app.utils.index_database import index_resources_by_transaction
from arches.app.utils.label_based_graph_v2 import LabelBasedGraph as LabelBasedGraphV2

logger = logging.getLogger(__name__)


class RDMMigrator(BaseBulkEditor):
    print("Hello World!")