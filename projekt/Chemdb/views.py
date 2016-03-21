#encoding: utf-8

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from rdkit import Chem
from rdkit.Chem import Draw

from Chemdb.models import Structure
from django.contrib import messages


from django.http import HttpResponseRedirect
from django.http import FileResponse

from django.shortcuts import render
from .forms import UploadFileForm
# Imaginary function to handle an uploaded file.
from .functions import handle_uploaded_file, handle_download_file


# Create your views here.
def structure_image(request, id):
    mol_obj = get_object_or_404(Structure, id=id)
    mol = Chem.MolFromSmiles(str(mol_obj.mol))
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
        print(request.FILES)
        if 'mol' in request.POST.keys():
            mol = Structure.objects.values_list('mol')
            r = (request.POST['mol'],)
            #print(r)
            #print(mol)
            if r in mol:
                messages.warning(request,r'Tato struktura je již v databázi')
                #return {'error_messages': error_messages}
            elif r == ('',):
                pass
            else:
                Structure(mol=request.POST['mol']).save()
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
                messages.warning(request,'Vyberte správný soubor')
                form = UploadFileForm()
    else:
        form = UploadFileForm()

    #structures = Structure.objects.all()
    return render(request, "Chemdb/insert.html", {"form": form})