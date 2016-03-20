#encoding: utf-8

from Chemdb.models import Structure
from rdkit import Chem

def handle_uploaded_file(file, type):
    with open('media/tmp.txt', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    odpoved = [0,0,0]
    mol = Structure.objects.values_list('mol')
    if type == 'SMILES':
        with open('media/tmp.txt', 'r') as soubor:
            for radka in soubor:
                if (radka,) in mol or radka == '':
                    odpoved[0] += 1
                elif Chem.MolFromSmiles(radka) == None:
                    odpoved[2] += 1
                else:
                    Structure(mol=radka).save()
                    odpoved[1] += 1
    else:
        soubor = Chem.SDMolSupplier('media/tmp.txt')
        for mlk in soubor:
            try:
                mlk = Chem.MolToSmiles(mlk)
            except:
                odpoved[2] += 1
            else:
                if (mlk,) in mol :
                    odpoved[0] += 1
                else:
                        Structure(mol=mlk).save()
                        odpoved[1] += 1
    return odpoved



