nome = "tuboDiSupporto_R01"
nome2 = "tuboDiSupporto_R05"
nome3 = "tuboDiSupporto"

stringa = nome.split("_")
stringa2 = nome2.split("_")
stringa3 = nome3.split("_")

print(stringa)
print(stringa2)
print(stringa3)

def stampa(lista):
    if len(lista) > 1:
        print(int("".join(filter(str.isdigit, lista[-1]))))

stampa(stringa)
stampa(stringa2)
stampa(stringa3)

print(stringa[1] < stringa2[1])