# interfaccia_parametri

## Obiettivo:

Finestra per la compilazione di dati da salvare su foglio excel e database

## Struttura della finestra:

Riferimento: Codice disegno (testo libero)
Codice padre: testo, assieme fittizio
Macchina: testo libero, facoltativo
Materiale: FERRO, INOX (legato a densità) associare a tabella esterna editabile
Denominazione profilo: menu a tendina con nomi standard
Data di creazione: (automatizzare)

Nome: ridondante, nome del cliente (facoltativo)
Codice: ridondante (facoltativo)
Cliente: associare a tabella esterna editabile
Q.tà per Disegno: valore numerico, default 1, editabile

Misura di massima: automatiche, vedi box ingombro (orientamento sempre uguale)
Massa: automatica, volume per densità (collegata a materiale)

## Suggerimenti:

Aggiungere salvataggio del file su percorso prestabilito, con creazione sottocartella in base al nome del cliente, quindi + proprietà di percorso file

Estrae immediatamente i dati e li immette nel database

Meglio gestire prima creazione e modifica con un unico tasto, quindi unica macro

## Installazione:

- Copiare il contenuto del repository all'interno della cartella macro di freecad
- Installare PyQT5 con il comando:
```python
pip install PyQT5
```
- Installare MySQL Python Connector con il comando: ```python pip install mysql-connector-python ```
