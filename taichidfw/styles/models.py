from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_lifecycle import BEFORE_SAVE, LifecycleModelMixin, hook
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

from taichidfw.locations.models import Location
from taichidfw.resources.models import Resource


class Style(LifecycleModelMixin, TimeStampedModel):
    title = models.CharField(
        "Title for TaiChi Style",
        max_length=90,
        unique=True,
        null=False,
        help_text="Short title for each TaiChi Style",
    )
    slug = models.SlugField(
        verbose_name="Style address", unique=True, default="Auto-generated"
    )
    description = models.TextField(verbose_name="Description", blank=True)
    wikipedia = models.URLField(verbose_name="Reference page.", blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = [
            "title",
        ]
        verbose_name = "style"
        verbose_name_plural = "styles"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("Styles:detail", kwargs={"slug": self.slug})

    @hook(BEFORE_SAVE, when="title", has_changed=True)
    def build_slug(self):
        newslug = slugify(self.title)
        if self.slug != newslug:
            self.slug = newslug


class StyleResource(TimeStampedModel):
    style = models.ForeignKey(
        Style, on_delete=models.CASCADE, related_name="styleResource"
    )
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="resourceStyle"
    )

    class Meta:
        verbose_name = "style_resource"
        verbose_name_plural = "style_resources"
        constraints = [
            models.UniqueConstraint(
                fields=["style", "resource"], name="unique style+resource"
            ),
        ]


class Series(LifecycleModelMixin, TimeStampedModel):
    title = models.CharField(
        "Title for TaiChi Series",
        max_length=90,
        unique=True,
        null=False,
        help_text="Short title for each TaiChi Series",
    )
    slug = models.SlugField(
        verbose_name="Series address", unique=True, default="Auto-generated"
    )
    style = models.ForeignKey(
        Style, on_delete=models.CASCADE, related_name="seriesStyle"
    )
    description = models.TextField(verbose_name="Description", blank=True)
    VISIBILITY_CHOICES = (
        ("public", "Show to public"),
        ("private", "Do not show to public"),
    )
    visibility = models.CharField(
        max_length=8,
        choices=VISIBILITY_CHOICES,
        default="private",
        help_text="Control whether guests can see this series.",
    )
    MEMBERSHIP_CHOICES = (
        ("open", "Open to all"),
        ("invite", "Leader must approve request to join"),
        ("closed", "Leader must add members"),
    )
    membership = models.CharField(
        max_length=8,
        choices=MEMBERSHIP_CHOICES,
        default="closed",
        help_text="Control how members are added to this series.",
    )
    take_roll = models.BooleanField("Allow leader to take roll", default=False)
    # Tags used by the leaders to describe the series for prospects
    tags = TaggableManager(
        "Tags to be searched to find your series",
        blank=True,
        help_text="Enter single word or 'quoted strings' to be used to find your series.",
    )

    class Meta:
        verbose_name = "series"
        verbose_name_plural = "series"
        indexes = [models.Index(fields=["style", "title"])]
        ordering = ["-visibility"]

    def __str__(self) -> str:
        return f"{self.style.title}: {self.title}"

    @hook(BEFORE_SAVE, when="title", has_changed=True)
    def build_slug(self):
        newslug = slugify(self.title)
        if self.slug != newslug:
            self.slug = newslug


class SeriesResource(TimeStampedModel):
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, related_name="seriesResource"
    )
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="resourceSeries"
    )

    class Meta:
        verbose_name = "series_resource"
        verbose_name_plural = "series_resources"
        constraints = [
            models.UniqueConstraint(
                fields=["series", "resource"], name="unique series+resource"
            ),
        ]


class Members(models.Model):
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="membersSeries"
    )
    series = models.ForeignKey(
        Series, related_name="seriesMembers", on_delete=models.CASCADE
    )
    leader = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    since = models.DateField(auto_now_add=True)
    last_meeting = models.DateField("Last meeting attended", null=True, blank=True)
    paid_through = models.DateField("Paid up through", null=True, blank=True)

    class Meta:
        verbose_name = "member"
        verbose_name_plural = "members"
        ordering = ["primary"]
        constraints = [
            models.UniqueConstraint(
                fields=["series", "member"], name="unique series+member"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.series.title}:{self.member.name}"


class Meeting(LifecycleModelMixin, TimeStampedModel):
    series = models.ForeignKey(
        "Series",
        on_delete=models.CASCADE,
        help_text="Series master for this meeting.",
        related_name="seriesMeetings",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Building where the meeting is held. Leave empty for virtual meetings.",
        related_name="meetingLocation",
    )
    room = models.TextField("Directions to meeting room or virtual link", blank=True)
    day = models.DateField("Date of last meeting", blank=True)
    start = models.TimeField("Start time of the meeting", blank=True)
    length = models.IntegerField("Minutes that the meeting lasts", blank=True)
    message = models.TextField(
        "Notes to be included in email / text reminders", default=""
    )
    leader = models.ForeignKey(
        Members, on_delete=models.SET_NULL, null=True, related_name="meetingLeader"
    )

    def __str__(self) -> str:
        return f"{self.series.title} on {self.day:%m/%d/%Y} leader:{self.leader.name}"

    class Meta:
        verbose_name = "meeting"
        verbose_name_plural = "meetings"
        get_latest_by = "day"
        ordering = ["-day"]


class MeetingAttendees(models.Model):
    attendee = models.ForeignKey(
        Members, on_delete=models.CASCADE, related_name="meetingAttendance"
    )
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, related_name="meetingRoll"
    )
    present = models.BooleanField(default=True)
    notes = models.TextField("Notes from the meeting - optional", default="")

    class Meta:
        verbose_name = "attendee"
        verbose_name_plural = "attendees"
        constraints = [
            models.UniqueConstraint(
                fields=["attendee", "meeting"], name="unique meeting attendee"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.meeting.series.title} on {self.meeting.day:%m/%d/%Y}, {self.attendee.member.name}"
