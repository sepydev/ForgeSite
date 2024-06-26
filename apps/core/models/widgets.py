from django.db import models
from django.db.transaction import atomic
from apps.common.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class WidgetManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class Widget(TimeStampedModel):
    objects = WidgetManager()

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(  # noqa : DJ01
        blank=True, null=True, verbose_name=_("Description")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Widget")
        verbose_name_plural = _("Widgets")
        ordering = ["-created_at"]

    @atomic
    def activate(self):
        self.is_active = True
        self.save(update_fields=["is_active"])

    @atomic
    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])
