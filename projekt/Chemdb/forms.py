from django import forms

SOUBOR = (
    ('SMILES', 'SMILES'),
    ('SDF', 'SDF'),
)

class UploadFileForm(forms.Form):

    #title = forms.CharField(max_length=50)
    file = forms.FileField(label="Soubor")
    type = forms.ChoiceField(label="Typ souboru", choices= SOUBOR )
