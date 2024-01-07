from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class WagtailSbAdminInterfaceConfig(AppConfig):
    name = "wagtail_sb_admin_interface"
    verbose_name = _("Wagtail Admin Interface")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from wagtail_sb_admin_interface import (  # pylint: disable=import-outside-toplevel
            settings,
        )
        from wagtail_sb_admin_interface.models import (  # pylint: disable=import-outside-toplevel
            Theme,
        )

        settings.check_installed_apps()
        post_migrate.connect(Theme.post_migrate_handler, sender=self)
