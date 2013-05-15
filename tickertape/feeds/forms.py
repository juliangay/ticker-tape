from django import forms

class UploadOpmlFileForm(forms.Form):
    file  = forms.FileField()