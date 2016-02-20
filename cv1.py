class Molekula(object):

    def __init__(self, sumarniVzorec):
        self.sumarniVzorec = sumarniVzorec
#slovnik prvek : pocet prvku v molekule
    def PrvkuMlk(self):
        pocetPrvku = {}
        for i in range(len(self.sumarniVzorec)):
            if self.sumarniVzorec[i].isnumeric():
                continue
            elif self.sumarniVzorec[i].islower():
                continue
            else:
                if self.sumarniVzorec[i] == self.sumarniVzorec[-1]:
                    pocetPrvku[self.sumarniVzorec[i]] = 1
                elif self.sumarniVzorec[i+1].islower():
                    prvek = self.sumarniVzorec[i] + self.sumarniVzorec[i+1]
                    if self.sumarniVzorec[i+1] == self.sumarniVzorec[-1]:
                        pocetPrvku[prvek] = 1
                    elif self.sumarniVzorec[i+2].isnumeric():
                        pocetPrvku[prvek] = self.sumarniVzorec[i+2]
                    else:
                        pocetPrvku[prvek] = 1
                elif self.sumarniVzorec[i+1].isnumeric():
                    pocetPrvku[self.sumarniVzorec[i]] = self.sumarniVzorec[i+1]
                else:
                    pocetPrvku[self.sumarniVzorec[i]] = 1
        return pocetPrvku

    def pocetAtomu(self,symbol="None"):
        pocetPrvku = Molekula.PrvkuMlk(self)
        if symbol == "None":
            soucet = 0
            for val in pocetPrvku.values():
                soucet += int(val)
            return soucet
        else:
            if symbol in pocetPrvku.keys():
                return int(pocetPrvku[symbol])
            else:
                return "Molekula neobsahuje dany symbol"

    def molekularniHmotnost(self):
        pocetPrvku = Molekula.PrvkuMlk(self)
        celkHmotnost = 0
        #soubuor obsahujici AtNo Symbol Name AtomicWt Notes
        with open("mlkVahy1.txt", mode="r",encoding="utf-8") as vahy:
            mlkHmotnsti = {}
            for v in vahy:
                v = v.split(" ")
                v1 = v[3].strip("[]")
                v1 = v1.split("(")
                v2 = v1[0]
                if v2 == "":
                    v2 = 0.0
                else:
                    v2 = float(v2)
                #slovnik obsahujici prvek : molekulova hmotnost
                mlkHmotnsti[v[1]] = v2
        for i in pocetPrvku.items():
            prvek = i[0]
            pocet = int(i[1])
            celkHmotnost += mlkHmotnsti[prvek] * pocet
            celkHmotnost = float("{0:.4f}".format(celkHmotnost))
        return celkHmotnost

    def sumarniVzorec(self):
          return self.sumarniVzorec

mol = Molekula("H2O")

assert mol.pocetAtomu() == 3
assert mol.pocetAtomu("H") == 2
assert mol.pocetAtomu("O") == 1
assert -1e-7 < mol.molekularniHmotnost() - 18 < 1e-1
assert mol.sumarniVzorec == "H2O"
print(mol.sumarniVzorec)
print(mol.pocetAtomu())
print(mol.pocetAtomu("H"))
print(mol.pocetAtomu("O"))
print(mol.pocetAtomu("He"))
print(mol.molekularniHmotnost())

