import logging
from celery import shared_task
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from arches.app.models import models
from arches_rdm.etl_modules import migrate_rdm


try:
    from arches.app.tasks import *
except ImportError:
    pass

@shared_task
def migrate_rdm(userid, load_id):

    logger = logging.getLogger(__name__)

    try:
        breakpoint()
        RDMMigrator = migrate_rdm.RDMMigrator(loadid=load_id)
        RDMMigrator.run_bulk_task(userid, load_id)

        load_event = models.LoadEvent.objects.get(loadid=load_id)
        status = _("Completed") if load_event.status == "indexed" else _("Failed")
    except Exception as e:
        logger.error(e)
        load_event = models.LoadEvent.objects.get(loadid=load_id)
        load_event.status = "failed"
        load_event.save()
        status = _("Failed")
    finally:
        msg = _("RDM Migration: [{}]").format(status)
        user = User.objects.get(id=userid)
        notify_completion(msg, user)
