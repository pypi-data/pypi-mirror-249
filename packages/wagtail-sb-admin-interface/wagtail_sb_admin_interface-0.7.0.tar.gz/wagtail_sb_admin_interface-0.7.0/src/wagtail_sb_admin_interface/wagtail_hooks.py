from django.utils.html import format_html
from wagtail import hooks

from .cache import get_cached_active_theme, set_cached_active_theme
from .models import Theme
from .views import theme_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return theme_viewset


@hooks.register("insert_global_admin_css")
def global_admin_css():
    theme = get_cached_active_theme()
    if not theme:
        theme = Theme.get_active_theme()
        set_cached_active_theme(theme)

    return format_html("<style>{}</style>", theme.css_styles)


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["wagtail_sb_admin_interface/icons/paintbrush-solid.svg"]
