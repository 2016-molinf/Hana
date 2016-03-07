from __future__ import unicode_literals

from django.db import models

from rdkit import Chem
from rdkit.Chem.Descriptors import MolWt

# Create your models here.

class Structure(models.Model):
   mol = models.TextField()

   def mol_weight(self):
       return MolWt(Chem.MolFromSmiles(str(self.mol)))