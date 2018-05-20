from datetime import date, time
from django import forms
from photologue.models import Gallery


class SearchForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ["from_datetime", "end_datetime"]

    galleries = [(g.title, g.title) for g in Gallery.objects.all() if g.public]
    gallery_selection = forms.CharField(widget=forms.Select(choices=galleries))
    from_datetime = forms.DateTimeField(
        initial=f"{date.today()} 00:00:00", widget=forms.TextInput()
    )
    end_datetime = forms.DateTimeField(
        initial=f"{date.today()} 00:00:00", widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["gallery_selection"].label = "Which camera gallery?"
        self.fields["from_datetime"].label = "Start Date"
        self.fields["end_datetime"].label = "End Date"
