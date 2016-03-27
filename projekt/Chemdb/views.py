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
from .forms import UploadFileForm,Search
# Imaginary function to handle an uploaded file.
from .functions import handle_uploaded_file, handle_download_file,handle_create_query

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
    structures = ''

    if request.method == "POST":
            #print(request.POST)
            #print(request.FILES)

            #print(request.FILES)
            #print(request.POST)
            form = Search(request.POST)
            if form.is_valid():
                dotaz,dotaz1 = handle_create_query(request.POST)
                #print(dotaz,dotaz1)

                if dotaz1 != '':
                    structures = Structure.objects.filter(**dotaz).exclude(**dotaz1)
                else:
                    structures = Structure.objects.filter(**dotaz)


                #messages.success(request, 'Soubor byl nahrán')
                #odpoved = handle_uploaded_file(request.FILES['file'],request.POST['type'] )
                #if type(odpoved) is str:
                ##
                # else:
                #messages.success(request, str(odpoved[1]) +r' struktur uloženo do databáze')
                #messages.warning(request, str(odpoved[0]) +r' ze struktur je již v databázi')
                #messages.warning(request, str(odpoved[2]) +r' chybných řádek souboru')
                #return HttpResponseRedirect('insert.html')
            else:
                messages.warning(request,r'Vyplňte všechna zvolená pole')
                form = Search()
    else:
        form = Search()


    return render(request, "Chemdb/search.html", {"form": form, "structures": structures})