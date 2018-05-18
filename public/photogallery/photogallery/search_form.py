from datetime import date, time
from django import forms
from photologue.models import Gallery


class SearchForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ["from_date", "from_time", "end_date", "end_time"]

    from_date = forms.DateTimeField(
        initial=f"{date.today()}", widget=forms.TextInput()
    )
    from_time = forms.TimeField(initial="00:00:00", widget=forms.TextInput())
    end_date = forms.DateTimeField(
        initial=f"{date.today()}", widget=forms.TextInput()
    )
    end_time = forms.TimeField(initial="00:00:00", widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["from_date"].label = "Start Date"
        self.fields["from_time"].label = "Start Time"
        self.fields["end_date"].label = "End Date"
        self.fields["end_time"].label = "End Time"
