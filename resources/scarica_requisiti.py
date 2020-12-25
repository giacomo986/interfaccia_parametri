import os, sys, subprocess

try:
    import mysql.connector
    print("modulo mysql connector trovato")
except:
    print("modulo mysql connector non trovato, provo a scaricarlo.")
    if os.name == "nt": # se la macro viene lanciata in ambiente windows
        subprocess.call([os.getcwd() + "//python -m pip install mysql-connector-python"], shell=True)
    else: # altrimenti siamo su linux
        try:
            subprocess.call([sys.executable + " -m pip install mysql-connector-python"], shell=True) # comando completo per l'installazione nella versione di python corretta
        except:
            subprocess.call(["pip install mysql-connector-python"], shell=True) # comando che funziona nell'Appimage
#finally:
#  import mysql.connector as mariadb
#  print("modulo mysql trovato")

try:
    import Equation
    print("modulo Equation trovato")
except:
    print("modulo Equation non trovato, provo a scaricarlo.")
    if os.name == "nt": # se la macro viene lanciata in ambiente windows
        subprocess.call([os.getcwd() + "//python -m pip install equation"], shell=True)
    else: # altrimenti siamo su linux
        try:
            subprocess.call([sys.executable + " -m pip install equation"], shell=True) # comando completo per l'installazione nella versione di python corretta
        except: 
            subprocess.call(["pip install equation"], shell=True) # comando che funziona nell'Appimage
