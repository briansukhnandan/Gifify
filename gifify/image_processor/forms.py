from django import forms


class VideoFileForm(forms.Form):
    docfile = forms.FileField(label='Select a file', required=True)
    optional_text = forms.CharField(max_length=50, label="Caption?", required=False)
    starting_timestamp = forms.IntegerField(help_text="Enter starting timestamp (seconds)", required=True)
    ending_timestamp = forms.IntegerField(help_text="Enter ending timestamp (seconds)", required=True)
    grayscale_option = forms.BooleanField(help_text="Grayscale?", required=False)
    pencil_sketched_option = forms.BooleanField(help_text="Pencil Sketched?", required=False)
    flipX_option = forms.BooleanField(help_text="Flip on the x-axis?", required=False)
    flipY_option = forms.BooleanField(help_text="Flip on the y-axis?", required=False)