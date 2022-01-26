from django.urls import path

from taichidfw.taichidfw.styles.views import (
    meeting_detail_view,
    series_detail_view,
    style_detail_view,
    style_list_view,
)

app_name = "styles"
urlpatterns = [
    path("series/<slug:slug>/", view=series_detail_view, name="series-detail"),
    path("meeting/<id:pk>/", view=meeting_detail_view, name="meeting-detail"),
    path("<slug:slug>/", view=style_detail_view, name="detail"),
    path("", view=style_list_view, name="list"),
]
