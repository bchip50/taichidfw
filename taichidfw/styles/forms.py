# from dfwtaichi.users.models import User
# from django import forms
# from django.conf import settings

# from .models import Series

"""
class SeriesMembersChangeListForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), required=False
    )


class SeriesLeadersChangeListForm(forms.ModelForm):
    leaders = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(leaderFlag=True)
    )


class MembersAttendeesChangeListForm(forms.ModelForm):
    here = forms.ModelMultipleChoiceField(queryset=Series.objects.("members"))
"""
