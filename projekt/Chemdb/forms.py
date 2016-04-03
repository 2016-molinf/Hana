from django import forms
#from .functions import validate_file_extension

SOUBOR = (
    ('SMILES', 'SMILES'),
    ('SDF', 'SDF'),
)
OPERATORY = (
    ('=','='),
    ('!=','!='),
    ('>=','>='),
    ('<=','<='),
    ('<','<'),
    ('>','>'),
)

class UploadFileForm(forms.Form):

    #title = forms.CharField(max_length=50)
    file = forms.FileField(label="Soubor")
    type = forms.ChoiceField(label="Typ souboru", choices= SOUBOR )

    def clean(self):
        data = self.cleaned_data['file']
        data1 = self.cleaned_data['type']
        #print(data)
        pripony = ['smi', 'smil', 'smiles', 'smile']
        pripona = data.name.split(".")
        #print(pripona)
        if data1 == 'SMILES':
            if data.content_type == 'text/plain' or pripona[1] in pripony:
                pass
            else:
                raise forms.ValidationError(u'Error message 123')
        else:
            if data.content_type != 'text/plain' and data.content_type != 'application/octet-stream':
                raise forms.ValidationError(u'Error message 123')

class Search(forms.Form):
    mol_name = forms.CharField(label="Název sloučeniny",required=False,widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-light-grey w3-hide', 'disabled':'true'}))
    opMW = forms.ChoiceField(label="Typ souboru", required=False, choices=OPERATORY, widget=forms.Select(attrs={'class':'w3-select w3-border w3-hide','disabled':'true'}))
    mol_weight = forms.DecimalField(label="Molekulová hmotnost", required=False, widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-light-grey w3-hide', 'step':'0.1', 'disabled':'true'}))
    mol_formula = forms.CharField(label="Vzorec sloučeniny", required=False, widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-light-grey w3-hide', 'disabled':'true'}))
    opSt = forms.ChoiceField(label="Typ souboru", required=False, choices=OPERATORY,widget=forms.Select(attrs={'class':'w3-select w3-border w3-hide', 'disabled':'true'}))
    mol_stock = forms.FloatField(label="Stav zásob",required=False, widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-light-grey w3-hide', 'disabled':'true'}))
    obrazek = forms.CharField(label="Nakreslit hledanou molekulu", required=False, widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-light-grey w3-hide','disabled':'true'}))

class Stock(forms.Form):
    mol_stock = forms.FloatField(label="Doplnit/Odebrat:", required=False, widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-light-grey w3-quarter','step':'0.1'}))
    #mol_id = forms.IntegerField(label="Stav zásob",required=False, widget=forms.NumberInput(attrs={'class':'w3-input w3-border w3-light-grey w3-hide', 'disabled':'true'}))