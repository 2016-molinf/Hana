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
        m = Chem.MolFromSmiles(m.mol)
        #m = Chem.MolToMolBlock(m)
        #print(m)
        writer.write(m)
    writer.close()
    return path, filename




