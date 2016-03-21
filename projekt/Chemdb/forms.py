from django import forms
#from .functions import validate_file_extension

SOUBOR = (
    ('SMILES', 'SMILES'),
    ('SDF', 'SDF'),
)

class UploadFileForm(forms.Form):

    #title = forms.CharField(max_length=50)
    file = forms.FileField(label="Soubor")
    type = forms.ChoiceField(label="Typ souboru", choices= SOUBOR )

    def clean(self):
        data = self.cleaned_data['file']
        print(data.content_type)
        if data.content_type != 'text/plain' and data.content_type != 'application/octet-stream':
            raise forms.ValidationError(u'Error message 123')
