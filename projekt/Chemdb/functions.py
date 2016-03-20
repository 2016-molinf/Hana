from Chemdb.models import Structure
from rdkit import Chem

def handle_uploaded_file(file, type):
    with open('media/tmp.txt', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    odpoved = [0,0]
    mol = Structure.objects.values_list('mol')
    if type == 'SMILES':
        with open('media/tmp.txt', 'r') as soubor:
            for radka in soubor:
                if (radka,) in mol or radka == '':
                    odpoved[0] += 1
                else:
                    Structure(mol=radka).save()
                    odpoved[1] += 1
    else:
        soubor = Chem.SDMolSupplier('media/tmp.txt')
        for mlk in soubor:
            if (Chem.MolToSmiles(mlk),) in mol :
                odpoved[0] += 1
            else:
                mlk = Chem.MolToSmiles(mlk)
                Structure(mol=mlk).save()
                odpoved[1] += 1
    return odpoved



