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
```shell
pip3 install PyQT5
```
- Installare MySQL Python Connector con il comando:
```shell
pip3 install mysql-connector-python
```
- Installare docker:
```shell
sudo apt install docker.io
```
- Abilitare l'avvio di docker all'avvio del sitema operativo:
```shell
sudo systemctl enable docker
```
- Aggiungere l'utente che esegue Docker al gruppo Docker per avere i diritti di eseguirlo. Riavviare il sistema operativo per aggiornare i diritti.
- Scaricare Mariadb per Docker:
```shell
docker pull mariadb/server
```
- Avviare la prima volta il container Mariadb:
```shell
docker run --name mariadbtest -e MYSQL_ROOT_PASSWORD=mypass -d mariadb/server
```
- Per Avviare, fermare o riavviare il container Mariadb:
```shell
docker start mariadbtest
```
```shell
docker stop mariadbtest
```
```shell
docker restart mariadbtest
```
- Il container Mariadbtest non si avvia automaticamente all'avvio del sistema operativo. Per fare ciò usiamo crontab:
```shell
crontab -e
```
- selezioniamo l'editor preferito e aggiungiamo la seguente riga in fondo al file di testo appena aperto:
```text
@reboot docker start mariadbtest
```

## Risorse utilizzate:

- Freecad 0.19: https://github.com/FreeCAD/FreeCAD/releases
- Docker: https://www.docker.com/
- Mariadb per docker:
https://mariadb.com/kb/en/installing-and-using-mariadb-via-docker/
https://hub.docker.com/_/mariadb
- GUI per Docker: https://github.com/docker/kitematic/releases 
- Esempi di codice Python per Mysql: https://www.w3schools.com/python/python_mysql_select.asp

## TODO list:

- ~~File di configurazione con percorso di salvataggio dei file~~
- ~~Funzione di estrazione dati da database~~
- ~~Maschera per la ricerca dei pezzi tramite database~~
- Funzione di riconoscimento revisioni vecchie da cancellare dal database (mantenere il file)
- Funzione e maschera per eliminazione manuale dei pezzi dal database
- gestione suffisso delle parti e gestione dell'indice di revisione
- il nome del file originale del cliente diventa il codice padre (assieme)
- Gestione delle eccezioni:
    - ~~mancata connessione al database e/o credenziali sbagliate~~
    - file linkato nel database non esistente
    - lista clienti vuota
    - lista materiali vuota
    - ~~file di configurazione mancante o vuoto e illegibile~~
    - percorso di salvataggio disegni non raggiungibile
    - permessi insufficienti percorso di salvataggio
    - ~~permessi insufficienti database~~ (non necessario)
