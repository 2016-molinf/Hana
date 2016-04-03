#encoding: utf-8

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw

from Chemdb.models import Structure
from django.contrib import messages


from django.http import HttpResponseRedirect
from django.http import FileResponse

from django.shortcuts import render
from .forms import UploadFileForm,Search,Stock
# Imaginary function to handle an uploaded file.
from .functions import handle_uploaded_file, handle_download_file,handle_create_query,handle_change_stock

from django.db.models import Q


# Create your views here.
def structure_image(request, id):
    mol_obj = get_object_or_404(Structure, id=id)
    #print(mol_obj.mol)
    mol = Chem.MolFromInchi(str(mol_obj.mol))
    #mol = Chem.MolFromMolBlock(str(mol_obj.mol))
    #print(mol)
    image = Draw.MolToImage(mol)
    response = HttpResponse(content_type="image/png")
    image.save(response,"PNG")
    return response


def index(request):
    structures = Structure.objects.all()
    if request.method == "POST":
        #print(request.POST)
        if 'mlk_all' in request.POST.keys() or 'mlk_id' in request.POST.keys():
            if 'mlk_all' in request.POST.keys():
                path, filename = handle_download_file(request.POST['mlk_all'])
            elif 'mlk_id' in request.POST.keys():
                path, filename = handle_download_file(request.POST.getlist('mlk_id'))
            #with open(path, mode="r", encoding="utf-8") as f:
                #response = HttpResponse(FileWrapper(f),content_type='application/download')
            response = FileResponse(open(path, 'rb'),content_type='application/download')
            response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            return response
        else:
            messages.warning(request,"Nevybrali jste žádnou sloučeninu")
    elif request.method == "GET":
        if request.GET.get('order_by',None):
            order = request.GET.get('order_by',None)
            print(order)
            structures = Structure.objects.all().order_by(order)



    #print(structures)
    return render(request, "Chemdb/structures.html", {"structures": structures})

#def search(request):
def insert(request):
        #print(Structure.objects.all())
    if request.method == "POST":
        #print(request.POST)
        #print(request.FILES)
        if 'mol' in request.POST.keys():
            mol = Structure.objects.values_list('mol')
            smi = Chem.MolFromSmiles(str(request.POST['mol']))
            r = (Chem.MolToInchi(smi),)
            #r = (Chem.MolToMolBlock(smi),)
            #print(r)
            #print(mol)
            if r in mol:
                messages.warning(request,r'Tato struktura je již v databázi')
                #return {'error_messages': error_messages}
            elif r == ('',):
                pass
            else:
                Structure(mol=Chem.MolToInchi(smi)).save()
                #AllChem.Compute2DCoords(smi)
                #mlk = Chem.MolToMolBlock(smi)
                #Structure(mol=mlk).save()
                messages.success(request, r'Struktura byla uložena do databáze')
            form = UploadFileForm()
        else:
            #print(request.FILES)
            #print(request.POST['type'])
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                messages.success(request, 'Soubor byl nahrán')
                odpoved = handle_uploaded_file(request.FILES['file'],request.POST['type'] )
                #if type(odpoved) is str:
                ##
                # else:
                messages.success(request, str(odpoved[1]) +r' struktur uloženo do databáze')
                messages.warning(request, str(odpoved[0]) +r' ze struktur je již v databázi')
                messages.warning(request, str(odpoved[2]) +r' chybných řádek souboru')
                #return HttpResponseRedirect('insert.html')
            else:
                messages.warning(request,r'Vyberte správný soubor')
                form = UploadFileForm()
    else:
        form = UploadFileForm()

    #structures = Structure.objects.all()
    return render(request, "Chemdb/insert.html", {"form": form})

def search(request):
    #print(Structure.objects.all())
    structures = []
    form = Search()

    if request.method == "POST":
        if 'mlk_all' in request.POST.keys() or 'mlk_id' in request.POST.keys():
            if 'mlk_all' in request.POST.keys():
                path, filename = handle_download_file(request.POST['mlk_all'])
            elif 'mlk_id' in request.POST.keys():
                path, filename = handle_download_file(request.POST.getlist('mlk_id'))
            #with open(path, mode="r", encoding="utf-8") as f:
                #response = HttpResponse(FileWrapper(f),content_type='application/download')
            response = FileResponse(open(path, 'rb'),content_type='application/download')
            response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            return response
        else:
            #print(request.POST)
            #print(request.FILES)
            form = Search(request.POST)
            if form.is_valid():
                dotaz,dotaz1 = handle_create_query(request.POST)
                print(dotaz,dotaz1)

                if dotaz1 != {}:
                    structures = Structure.objects.filter(**dotaz).exclude(**dotaz1)
                elif dotaz == {}:
                    pass
                else:
                    structures = Structure.objects.filter(**dotaz)
                print(structures)
                try:
                    structures[0]
                except:
                    messages.warning(request, 'Nic nenalezeno')
            else:
                #messages.warning(request,r'Vyplňte všechna zvolená pole')
                form = Search()
    elif request.method == "GET":
        try:
            structures[0]
        except:
            pass
        else:
            if request.GET.get('order_by',None):
                order = request.GET.get('order_by',None)
                structures = Structure.objects.all().order_by(order)

    return render(request, "Chemdb/search.html", {"form": form, "structures": structures})

def chemical(request):
    form = Stock()
    structures = []
    if request.method == "POST":
        form = Stock(request.POST)
        if form.is_valid():
            #print("a",request.POST)
            if request.POST['mol_stock'] == '' and request.POST['get_id'] != '':
                path, filename = handle_download_file(request.POST.getlist('get_id'))
                response = FileResponse(open(path, 'rb'),content_type='application/download')
                response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
                #return response
            elif request.POST['mol_stock'] == '' and request.POST['get_id'] == '':
                messages.warning(request, str(r' Nezadali jste žádnou hodnotu'))
            elif request.POST['mol_stock'] != '' and request.POST['get_id'] != '':
                #print(request.POST['mol_stock'])
                change, path, filename = handle_change_stock(request.POST['mol_stock'],request.POST['get_id'])
                if change < 0:
                     messages.warning(request, str(r'Na skladě je o  ')+str(round(abs(change),3))+str(r' ml méně než požadujete'))
                     messages.warning(request, str(r'Pro doplnění zásob kontaktujte obsluhu skladu'))
                elif float(request.POST['mol_stock']) < 0 and change > 0:
                    #messages.success(request, str(r'Děkujeme, informace o objednávce naleznete v právě staženém pdf '))
                    response = FileResponse(open(path, 'rb'),content_type='application/download')
                    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
                    #return response
                elif float(request.POST['mol_stock']) > 0:
                    messages.success(request, str(r'Na skladě je nyní o  ')+str(round(abs(change),3))+str(r' ml více'))


    #if request.method == "GET":
    if request.GET.get('chem_id',None):
        chem_id = request.GET.get('chem_id',None)
        structures = Structure.objects.filter(id=chem_id)
        #print("b", chem_id, structures)
    try:
        response
    #print("c",structures)#, "structures": structures}
    except:
        return render(request, "Chemdb/chemical.html", {"form": form, "structures": structures})
    else:
        return response
def about(request):
    return render(request, "Chemdb/about.html")
def contact(request):
    return render(request, "Chemdb/contact.html")