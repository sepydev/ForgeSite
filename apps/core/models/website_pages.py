from django.db import models
from django.db.transaction import atomic

from apps.common.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class WebsiteManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    @atomic
    def create_landing_page(self, title, slug):
        self.filter(landing_page=True).update(active=False)
        return self.create(title=title, slug=slug, landing_page=True)

    def landing_pages(self):
        return self.filter(landing_page=True)


class WebsitePage(TimeStampedModel):
    objects = WebsiteManager()

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_("Slug"))
    landing_page = models.BooleanField(default=False, verbose_name=_("Landing Page"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Website Page")
        verbose_name_plural = _("Website Pages")
        ordering = ["-created_at"]

    @atomic
    def set_as_landing_page(self):
        self.objects.landing_pages().active().update(active=False)
        self.landing_page = True
        self.is_active = True
        self.save(update_fields=["landing_page", "is_active"])
