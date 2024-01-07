from django.conf import settings
from django.core.cache import cache, caches


def app_cache():
    return (
        caches["wagtail_sb_admin_interface"]
        if "wagtail_sb_admin_interface" in settings.CACHES
        else cache
    )


def del_cached_active_theme():
    app_cache().delete("wagtail_sb_admin_interface_theme")


def get_cached_active_theme():
    return app_cache().get("wagtail_sb_admin_interface_theme", None)


def set_cached_active_theme(theme):
    app_cache().set("wagtail_sb_admin_interface_theme", theme)
