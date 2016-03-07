from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from rdkit import Chem
from rdkit.Chem import Draw

from Chemdb.models import Structure

# Create your views here.

def structure_image(request, id):
    mol_obj = get_object_or_404(Structure, id=id)
    mol = Chem.MolFromSmiles(str(mol_obj.mol))
    image = Draw.MolToImage(mol)
    response = HttpResponse(content_type="image/png")
    image.save(response,"PNG")
    return response

def index(request):
    if request.method == "POST":
        #print(request.POST['mol'])
        mol = Structure.objects.values_list('mol')
        r= (request.POST['mol'],)
        print(r)
        #print(mol)
        if r in mol or r == ('',):
            pass
        else:
            Structure(mol=request.POST['mol']).save()

    structures = Structure.objects.all()
    return render(request, "Chemdb/structures.html", {"structures": structures})