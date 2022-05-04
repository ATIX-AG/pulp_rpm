from gettext import gettext as _
from django.db.models.signals import post_migrate
from pulpcore.plugin import PulpPluginAppConfig


def _unapply_migration(sender, **kwargs):
    """
    This function is intended for use with backported migrations, that now need to be applied out of
    order. To satisfy pulpcore-admin migrate's check for correct order, we mark this migration as
    unapplied after we have just applied it. The pre-requisite for this approach is that it does not
    matter how many times the migration in question is applied.
    """
    from django.db import connection

    migration_name = "0042_alter_repometadatafile_data_type"
    with connection.cursor() as cursor:
        sql = "DELETE FROM django_migrations WHERE name='{}';".format(migration_name)
        cursor.execute(sql)
    print(_("Setting backported migration '{}' as unapplied!").format(migration_name))


class PulpRpmPluginAppConfig(PulpPluginAppConfig):
    """
    Entry point for pulp_rpm plugin.
    """

    name = "pulp_rpm.app"
    label = "rpm"
    version = "3.17.6.dev"

    def ready(self):
        super().ready()
        post_migrate.connect(_unapply_migration, sender=self)
