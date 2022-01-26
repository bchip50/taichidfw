from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_lifecycle import BEFORE_SAVE, LifecycleModelMixin, hook
from model_utils.models import TimeStampedModel


class Resource(LifecycleModelMixin, TimeStampedModel):
    title = models.CharField(
        "Short title for resource",
        max_length=90,
        unique=True,
        null=False,
        help_text="Short title for each resource",
    )
    slug = models.SlugField(
        verbose_name="Resource address", unique=True, default="Auto-generated"
    )
    description = models.TextField(verbose_name="Description", blank=True)
    VISIBILITY_CHOICES = (
        ("public", "Show to public"),
        ("private", "Show to members only."),
    )
    visibility = models.CharField(
        max_length=8,
        choices=VISIBILITY_CHOICES,
        default="private",
        help_text="Control whether guests can see this resource.",
    )
    RESOURCE_TYPE = (
        ("website", "Website useful for this style or series."),
        ("book", "Link to page where the book can be purchased"),
        ("slideshow", "Slide show of photos or presentation"),
        ("video", "Link to video"),
        ("photo", "Link to single photo"),
        ("store", "Link to the store website"),
        ("tournament", "Link to tournament website"),
        ("none", "Resource does not have a link"),
    )
    link_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE,
        default="none",
        help_text="Classification of this link by type for sub-menus.",
    )
    link = models.URLField("Link address to be used under the description", blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "resource"
        verbose_name_plural = "resources"

    def get_absolute_url(self):
        return reverse("resources.views.detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.link_type}:{self.title}"

    @hook(BEFORE_SAVE, when="title", has_changed=True)
    def build_slug(self):
        newslug = slugify(self.title)
        if self.slug != newslug:
            self.slug = newslug
