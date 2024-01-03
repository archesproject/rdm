from arches.app.models import models


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("models", "10121_workflowhistory"),
    ]

    def add_plugins(apps, schema_editor):
        Plugin = apps.get_model("models", "Plugin")

        Plugin.objects.update_or_create(
            pluginid="29321ce0-bd95-4357-a2a5-822e9cb06f70",
            name="Reference Data Manager (RDM)",
            icon="fa fa-code-fork",
            component="views/components/plugins/reference-data-manager",
            componentname="reference-data-manager",
            config={},
            slug="reference-data-manager",
            sortorder=0
        )

    def remove_plugin(apps, schema_editor):
        Plugin = apps.get_model("models", "Plugin")

        for plugin in Plugin.objects.filter(pluginid__in=["29321ce0-bd95-4357-a2a5-822e9cb06f70"]):
            plugin.delete()

    operations = [
        migrations.RunPython(add_plugins, remove_plugin),
    ]