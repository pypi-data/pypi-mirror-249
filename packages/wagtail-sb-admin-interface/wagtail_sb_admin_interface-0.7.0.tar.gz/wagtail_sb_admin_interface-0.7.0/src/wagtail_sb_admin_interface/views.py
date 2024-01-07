from wagtail.admin.viewsets.model import ModelViewSet

from .models import Theme


class ThemeViewSet(ModelViewSet):
    model = Theme
    form_fields = "__all__"
    menu_label = "Themes"
    menu_icon = "paint-brush"
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = (
        "name",
        "active",
    )
    list_filter = ("active",)
    search_fields = ("name",)


theme_viewset = ThemeViewSet("theme")
