#encoding: utf-8

from Chemdb.models import Structure
from rdkit import Chem
from rdkit.Chem import AllChem
from reportlab.pdfgen import canvas


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
            print(mlk)
            mol = Structure.objects.values_list('mol')
            try:
                #mlk = Chem.MolToSmiles(mlk)
                mlk = Chem.MolToInchi(mlk)
                print("a",mlk)
                #AllChem.Compute2DCoords(mlk)
                #mlk = Chem.MolToMolBlock(mlk)
            except:
                odpoved[2] += 1
            else:
                if mlk == "":
                    odpoved[2] += 1
                elif (mlk,) in mol :
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

def handle_create_query(request):
    dotaz = ''
    dotaz1 = ''
    dotaz2 = {}
    dotaz3 = {}
    ex = False

    for i in request:
        if i =='csrfmiddlewaretoken':
            next
        elif i == 'opMW':
            if request['opMW'] == ">":
                dotaz = "mol_weight__gt"
            elif request['opMW'] == ">=":
                dotaz = "mol_weight__gte"
            elif request['opMW'] == "<":
                dotaz = "mol_weight__lt"
            elif request['opMW'] == ">=":
                dotaz = "mol_weight__lte"
            elif request['opMW'] == "!=":
                dotaz = "mol_weight"
                ex = True
            elif request['opMW'] == "=":
                dotaz = "mol_weight"
        elif i == 'opSt':
            if request['opSt'] == ">":
                dotaz = "mol_stock__gt"
            elif request['opSt'] == ">=":
                dotaz = "mol_stock__gte"
            elif request['opSt'] == "<":
                dotaz = "mol_stock__lt"
            elif request['opSt'] == ">=":
                dotaz = "mol_stock__lte"
            elif request['opSt'] == "!=":
                dotaz = "mol_stock"
                ex = True
            elif request['opSt'] == "=":
                dotaz = "mol_stock"
        elif i == "obrazek":
            d = Chem.MolFromSmiles(request[i])
            mols = {}
            for x in Structure.objects.all():
                mols[x.id]=Chem.MolFromInchi(x.mol)
            match = {k: d.HasSubstructMatch(v)for k, v in mols.items()}
            klice = [k for k, v in match.items() if v]
            dotaz2["id__in"] = klice
        elif i == "mol_formula":
            dotaz2["mol_formula"] = str(request[i])
        elif i == "mol_name":
            dotaz2["mol_name"] = str(request[i])
        else:
            dotaz1 = str(request[i])

        if dotaz1 != '' and dotaz != '':
            if ex:
                dotaz3[dotaz] = dotaz1
                ex = False
            else:
                dotaz2[dotaz] = dotaz1
            dotaz = ''
            dotaz1 = ''
    return dotaz2, dotaz3

def handle_change_stock(request,id):
    folder = "media/"
    mapa = "Chemdb/static/obr/pata_mapa.jpg"
    mlk = Structure.objects.get(id=id)
    filename = "Objednavka_MINF-HD-{}.pdf".format(mlk.id)
    path = folder + filename
    change = mlk.mol_stock
    change += float(request)
    if change < 0:
        return change,path, filename
    else:
        if float(request) < 0:
            p = canvas.Canvas(path)
            #p.drawString(100, 100, "Hello world.")
            p.setFont("Helvetica", 25)
            p.drawString(230, 790,"Objednávka")
            p.setFont("Helvetica", 14)
            p.drawString(10, 750,"ID: MINF-HD-"+str(mlk.id))
            p.drawString(10, 730,"Objednáno: "+str(abs(float(request)))+" ml")
            p.drawString(10, 710,"Místo vyzvednutí: Budova A")
            p.drawImage(mapa, 10,450, width=170,height=240,mask=None)
            p.showPage()
            p.save()
            """
            with open(path,mode="w",encoding="utf-8") as obj:
                obj.write("Objednávka")
                obj.write("ID: MINF-HD-"+str(mlk.id))
                obj.write("Objednáno: "+str(abs(change))+" ml")
                obj.write("Místo vyzvednutí:")
                #obj.write(obrazek)
            """
        mlk.mol_stock += float(request)
        mlk.save()
        return change, path, filename











