from django.contrib import admin

# from taichidfw.locations.models import Location
# from taichidfw.resources.models import Resource
from taichidfw.styles.models import Meeting, Members, Series, Style

"""
from taichidfw.styles.forms import (
    MembersAttendeesChangeListForm,
    SeriesMembersChangeListForm,
    SeriesLeadersChangeListForm,
)


class SeriesMembersChangeList:
    def __init__(
        self,
        request,
        model,
        list_display,
        list_display_link,
        list_filter,
        date_hierarchy,
        search_fields,
        list_selected_related,
        list_per_page,
        list_max_show_all,
        list_editable,
        model_admin,
    ):
        super(SeriesMembersChangeList, self).__init__(
            request,
            model,
            list_display,
            list_display_link,
            list_filter,
            date_hierarchy,
            search_fields,
            list_selected_related,
            list_per_page,
            list_max_show_all,
            list_editable,
            model_admin,
        )
        self.list_display = ["action_checkbox", "title", "members"]
        self.list_display_links = ["slug"]
        self.list_editable = ["members"]
"""


class SeriesInLine(admin.TabularInline):
    model = Series
    min_num = 0


@admin.register(Style)
class StylesAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
    ]
    inlines = [SeriesInLine]


class SeriesMembersInLine(admin.TabularInline):
    model = Members
    min_num = 0


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = [
        "style",
        "title",
        "slug",
    ]
    inlines = [
        SeriesMembersInLine,
    ]


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ["series", "day"]
