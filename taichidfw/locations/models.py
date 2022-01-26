from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_google_maps import fields as map_fields
from django_lifecycle import BEFORE_SAVE, LifecycleModelMixin, hook
from model_utils.models import TimeStampedModel
from phone_field import PhoneField


class LocContact(models.Model):
    contact = models.CharField(
        "Name of the primary contact",
        max_length=100,
        blank=True,
        help_text="Full name of the primary contact.",
    )
    contact_email = models.EmailField(
        "Email address of the primary contact", blank=True
    )
    contact_phone = PhoneField("Work phone number for the location", blank=True)

    class Meta:
        abstract = True


class Gmaps(models.Model):
    address = map_fields.AddressField(max_length=200, blank=True)
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True)

    class Meta:
        abstract = True


class Location(LifecycleModelMixin, TimeStampedModel, LocContact, Gmaps, models.Model):
    title = models.CharField(
        "Name of the location.",
        max_length=120,
        unique=True,
        help_text="Formal name for the location.",
    )
    slug = models.SlugField(
        verbose_name="Location address", unique=True, default="Auto-generated"
    )
    address1 = models.CharField("Street Address line 1", max_length=120, blank=True)
    address2 = models.CharField("Street Address line 1", max_length=120, blank=True)
    city = models.CharField("City", max_length=50, blank=True)
    state = models.CharField("State", max_length=2, default="Tx")
    zipcode = models.CharField("Zip code", max_length=5, blank=True)

    def __str__(self):
        return f"{self.title} in {self.city}"

    @hook(BEFORE_SAVE, when="title", has_changed=True)
    def build_slug(self):
        newslug = slugify(self.title)
        if self.slug != newslug:
            self.slug = newslug

    def get_absolute_url(self):
        return reverse("locations.views.detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "location"
        verbose_name_plural = "locations"
