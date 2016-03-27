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
    mol_stock = models.PositiveIntegerField(default=0)
    #mol = models
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
        a = Chem.MolFromInchi(str(self.mol))
        #a = Chem.MolFromMolBlock(str(self.mol))
        self.mol_weight = MolWt(a)
        self.mol_formula = CalcMolFormula(a)
        #print(self.mol_formula)
        return super(self.__class__, self).save()

    def mol_id(self):
        return "MINF-HD-{}".format(self.id)

    def round_mol_weight(self):
        return round(self.mol_weight,3)
"""
    def save_to_file(self,iddb):
        data = Chem.MolToMolFile(Chem.MolFromSmiles(str(self.mol)))
        with open(iddb+".mol",mode="w",encoding="utf-8") as f:
            f.write(data)

"""

   #def mol_formula(self):
    #   return CalcMolFormula(Chem.MolFromSmiles(str(self.mol))) #jednodusi ale neda se podle toho vzhledavat pokud chceme musime dat do db jako dalsi pole

