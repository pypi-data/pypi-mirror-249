from __future__ import unicode_literals

import colorsys
from dataclasses import dataclass

from colorfield.fields import ColorField
from django.db import models
from django.db.models import TextChoices
from django.db.models.signals import post_delete, post_save, pre_save
from django.utils.translation import gettext_lazy as _
from six import python_2_unicode_compatible
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string

from wagtail_sb_admin_interface.cache import del_cached_active_theme
from wagtail_sb_admin_interface.compat import force_str


@dataclass
class HLS:
    # pylint: disable=invalid-name
    """A dataclass for representing HLS colors."""

    H: float = 0
    L: float = 0
    S: float = 0

    @classmethod
    def from_hex(cls, hex_color: str) -> "HLS":
        """Create a HLS color from a hex color."""
        RGB = tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
        rgb = tuple(c / 255.0 for c in RGB)
        hls = colorsys.rgb_to_hls(*rgb)
        return cls(hls[0] * 360, hls[1] * 100, hls[2] * 100)


class SidebarLogoShape(TextChoices):
    """Choices for the sidebar logo shape."""

    ORIGINAL = "", _("Original")

    CIRCULAR = "circular", _("Circular")
    RECTANGULAR = "rectangular", _("Rectangular")
    SQUARE = "square", _("Square")


@python_2_unicode_compatible
class Theme(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        default="Wagtail",
        verbose_name=_("name"),
    )

    active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
    )

    # -------------------------------------------------------------------------
    # Wagtail branding
    # -------------------------------------------------------------------------
    sidebar_logo = models.ForeignKey(
        get_image_model_string(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo"),
    )

    sidebar_logo_collapsed = models.ForeignKey(
        get_image_model_string(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo (collapsed)"),
    )

    sidebar_logo_shape = models.CharField(
        blank=True,
        choices=SidebarLogoShape.choices,
        default=SidebarLogoShape.ORIGINAL,
        max_length=50,
        verbose_name=_("Shape of logo"),
    )

    sidebar_logo_background_color = ColorField(
        blank=True,
        default="#ffffff",
        max_length=10,
        verbose_name=_("Background color"),
    )

    # -------------------------------------------------------------------------
    # Wagtail colors
    # -------------------------------------------------------------------------
    color_primary = ColorField(
        blank=True,
        default="#2e1f5e",
        max_length=10,
        verbose_name=_("Primary color"),
    )

    color_secondary = ColorField(
        blank=True,
        default="#007d7e",
        max_length=10,
        verbose_name=_("Secondary color"),
    )

    # -------------------------------------------------------------------------
    # Wagtail colors
    # -------------------------------------------------------------------------
    color_info = ColorField(
        blank=True,
        default="#1f7e9a",
        max_length=10,
        verbose_name=_("Informative color"),
    )

    color_positive = ColorField(
        blank=True,
        default="#1b8666",
        max_length=10,
        verbose_name=_("Positive color"),
    )

    color_warning = ColorField(
        blank=True,
        default="#faa500",
        max_length=10,
        verbose_name=_("Warning color"),
    )

    color_critical = ColorField(
        blank=True,
        default="#cd4444",
        max_length=10,
        verbose_name=_("Critical color"),
    )

    # -------------------------------------------------------------------------
    # Wagtail Fields
    # -------------------------------------------------------------------------
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("active"),
            ],
            heading=_("Theme"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("sidebar_logo"),
                FieldPanel("sidebar_logo_collapsed"),
                FieldPanel("sidebar_logo_shape"),
                FieldPanel("sidebar_logo_background_color"),
                FieldPanel("color_primary"),
                FieldPanel("color_secondary"),
            ],
            heading=_("Branding"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("color_info"),
                FieldPanel("color_positive"),
                FieldPanel("color_warning"),
                FieldPanel("color_critical"),
            ],
            heading=_("Informative colors"),
        ),
    ]

    def set_active(self):
        self.active = True
        self.save()

    class Meta:
        app_label = "wagtail_sb_admin_interface"

        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

    def __str__(self):
        return force_str(self.name)

    @property
    def css_styles(self) -> str:
        primary = HLS.from_hex(self.color_primary)
        secondary = HLS.from_hex(self.color_secondary)
        info = HLS.from_hex(self.color_info)
        positive = HLS.from_hex(self.color_positive)
        warning = HLS.from_hex(self.color_warning)
        critical = HLS.from_hex(self.color_critical)

        return f"""
            :root {{
                --w-color-primary-hue: {primary.H};
                --w-color-primary-saturation: {primary.S}%;
                --w-color-primary-lightness: {primary.L}%;

                --w-color-secondary-hue: {secondary.H};
                --w-color-secondary-saturation: {secondary.S}%;
                --w-color-secondary-lightness: {secondary.L}%;

                --w-color-info-100-hue: {info.H};
                --w-color-info-100-saturation: {info.S}%;
                --w-color-info-100-lightness: {info.L}%;

                --w-color-positive-100-hue: {positive.H};
                --w-color-positive-100-saturation: {positive.S}%;
                --w-color-positive-100-lightness: {positive.L}%;

                --w-color-warning-100-hue: {warning.H};
                --w-color-warning-100-saturation: {warning.S}%;
                --w-color-warning-100-lightness: {warning.L}%;

                --w-color-critical-200-hue: {critical.H};
                --w-color-critical-200-saturation: {critical.S}%;
                --w-color-critical-200-lightness: {critical.L}%;
            }}
        """

    @staticmethod
    def post_migrate_handler(**kwargs):
        del_cached_active_theme()
        Theme.get_active_theme()

    @staticmethod
    def post_delete_handler(**kwargs):
        del_cached_active_theme()
        Theme.get_active_theme()

    @staticmethod
    def post_save_handler(instance, **kwargs):
        del_cached_active_theme()
        if instance.active:
            Theme.objects.exclude(pk=instance.pk).update(active=False)
        Theme.get_active_theme()

    @staticmethod
    def pre_save_handler(instance, **kwargs):
        if instance.pk is None:
            try:
                obj = Theme.objects.get(name=instance.name)
                if obj:
                    instance.pk = obj.pk
            except Theme.DoesNotExist:
                pass

    @staticmethod
    def get_active_theme():
        objs_manager = Theme.objects
        objs_active_qs = objs_manager.filter(active=True)
        objs_active_ls = list(objs_active_qs)
        objs_active_count = len(objs_active_ls)

        if objs_active_count == 0:
            obj = objs_manager.all().first()
            if obj:
                obj.set_active()
            else:
                obj = objs_manager.create()

        elif objs_active_count == 1:
            obj = objs_active_ls[0]

        elif objs_active_count > 1:
            obj = objs_active_ls[-1]
            obj.set_active()

        return obj


post_delete.connect(Theme.post_delete_handler, sender=Theme)
post_save.connect(Theme.post_save_handler, sender=Theme)
pre_save.connect(Theme.pre_save_handler, sender=Theme)
