from __future__ import unicode_literals

from django.db import models

from rdkit import Chem
from rdkit.Chem.Descriptors import MolWt
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

# Create your models here.

class Structure(models.Model):
    mol = models.TextField()
    mol_formula = models.TextField(default="NA")
    mol_weight = models.FloatField(default=0)
    """
    def __init__(self, mol):
        super(self.__class__, self).__init__(
            mol=mol,
            mol_formula=CalcMolFormula(Chem.MolFromSmiles(str(mol))),
            mol_weight=MolWt(Chem.MolFromSmiles(str(mol)))
        )
    """
    def save(self):
        #print(self.mol)
        self.mol_weight = MolWt(Chem.MolFromSmiles(str(self.mol)))
        self.mol_formula = CalcMolFormula(Chem.MolFromSmiles(str(self.mol)))
        #print(self.mol_formula)
        return super(self.__class__, self).save()

    def mol_id(self):
        return "MINF-HD-{}".format(self.id)

    def round_mol_weight(self):
        return round(self.mol_weight,3)

   #def mol_formula(self):
    #   return CalcMolFormula(Chem.MolFromSmiles(str(self.mol))) #jednodusi ale neda se podle toho vzhledavat pokud chceme musime dat do db jako dalsi pole

