from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FlatPagesConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "django_async_extensions.acontrib.flatpages"
    verbose_name = _("Flat Pages")
