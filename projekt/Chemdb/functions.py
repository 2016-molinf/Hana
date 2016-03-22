#encoding: utf-8

from Chemdb.models import Structure
from rdkit import Chem
from rdkit.Chem import AllChem


def handle_uploaded_file(file, type):
    with open('media/tmp.txt', 'wb+') as destination:
        if type == 'SMILES':
            destination.write(b'hlavicka\n')
        for chunk in file.chunks():
            destination.write(chunk)

    odpoved = [0,0,0]
    #mol = Structure.objects.values_list('mol')
    #print(mol)
    if type == 'SMILES':
        soubor = Chem.SmilesMolSupplier('media/tmp.txt')
        for mlk in soubor:
            mol = Structure.objects.values_list('mol')
            try:
                mlk = Chem.MolToInchi(mlk)
                #AllChem.Compute2DCoords(mlk)
                #mlk = Chem.MolToMolBlock(mlk)
            except:
                odpoved[2] += 1
            else:
                if (mlk,) in mol :
                    odpoved[0] += 1
                else:
                        Structure(mol=mlk).save()
                        odpoved[1] += 1
    else:
        soubor = Chem.SDMolSupplier('media/tmp.txt')
        for mlk in soubor:
            #print(mlk)
            mol = Structure.objects.values_list('mol')
            try:
                mlk = Chem.MolToInchi(mlk)
               # AllChem.Compute2DCoords(mlk)
                #mlk = Chem.MolToMolBlock(mlk)
            except:
                odpoved[2] += 1
            else:
                if (mlk,) in mol :
                    odpoved[0] += 1
                else:
                        Structure(mol=mlk).save()
                        odpoved[1] += 1
    return odpoved

def handle_download_file(request):
    folder = "media/"
    #print(request)
    if request == 'all':
        mlk = Structure.objects.all()
        filename = "Chemdb_all.sdf"
    elif len(request) == 1:
        mlk = Structure.objects.filter(id=int(request[0]))
        filename = "Chemdb_MINF-HD-{}.sdf".format(mlk[0].id)
    else:

        mlk = Structure.objects.filter(id__in=request)
        filename = "Chemdb_{}_struktur.sdf".format(len(mlk))

    path = folder + filename
    writer = Chem.SDWriter(path)
    for m in mlk:
        m = Chem.MolFromInchi(str(m.mol))
        AllChem.Compute2DCoords(m)
        #m = Chem.MolToMolBlock(str(m.mol))
        #m = Chem.MolToMolBlock(m)
        #m=str(m.mol)
        #print(m)
        writer.write(m)
    writer.close()
    return path, filename






