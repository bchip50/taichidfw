# from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import (  # SeriesResource, Style, StyleResource, Members
    Meeting,
    Series,
    Style,
)


class StyleListView(ListView):
    model = Style


style_list_view = StyleListView.as_view()


class ActiveSeriesMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sty = context["style"]
        context["resources"] = sty.styleResource.all()
        ser = sty.seriesStyle.all()
        for s in ser:
            s["members"] = s.Members.all()
            s["resources"] = s.seriesResoures.all()
        context["series"] = ser

        return context


class StyleDetailView(ActiveSeriesMixin, DetailView):
    model = Style


style_detail_view = StyleDetailView.as_view()


class ActiveLeadersMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actl = context["series"]
        context["active_leaders"] = actl.seriesMembers.filter(leader_is=True)
        context["active_members"] = actl.seriesMembers.filter(
            active_is=True, leader_is=False
        )
        return context


class SeriesDetailView(ActiveLeadersMixin, DetailView):
    model = Series


series_detail_view = SeriesDetailView.as_view()


class MeetingDetailView(ActiveLeadersMixin, DetailView):
    model = Meeting


meeting_detail_view = MeetingDetailView.as_view()
