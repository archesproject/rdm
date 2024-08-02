from django.apps import AppConfig

from arches.settings_utils import generate_frontend_configuration


class Arches_LingoConfig(AppConfig):
    name = "arches_lingo"
    verbose_name = "Arches Lingo"
    is_arches_application = True

    def ready(self):
        generate_frontend_configuration()
