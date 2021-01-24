# interfaccia_parametri

## Obiettivo:

Finestra per la compilazione di dati da salvare su database.

## Installazione prerequisiti:


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
```shell
sudo usermod -aG docker $USER
```
- Scaricare Mariadb per Docker:
```shell
docker pull mariadb/server
```
- Avviare la prima volta il container Mariadb:
```shell
docker run --name mariadbtest -e MYSQL_ROOT_PASSWORD=mypass -d -p 3306:3306  mariadb/server
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
- Per accedere alla linea di comando del container:
```shell
docker exec -it mariadbtest bash
```
- Per accedere direttamente al database nel container: 
```shell
mysql -h 127.0.0.1 -u root -p
```
- Creare un utente non amministratore all'interno di MariaDB: 
```sql
CREATE USER 'freecad'@'%' IDENTIFIED BY 'freecad';
```
Il simbolo '**%**' indica che l'utente è accessibile anche al di fuori del container.
- Creare un database per la macro:
```sql
CREATE DATABASE DBPezzi;
```
- Coferire poteri d'accesso all'utente appena creato:
```sql
GRANT ALL PRIVILEGES ON DBPezzi . * TO 'freecad'@'%';
```
## Risorse utilizzate:

- Freecad 0.19: https://github.com/FreeCAD/FreeCAD/releases
- Docker: https://www.docker.com/
- Mariadb per docker:
https://mariadb.com/kb/en/installing-and-using-mariadb-via-docker/
https://hub.docker.com/_/mariadb
- GUI per Docker: https://github.com/docker/kitematic/releases 
- Esempi di codice Python per Mysql: https://www.w3schools.com/python/python_mysql_select.asp

## Istruzioni:

La Macro consiste in 2 finestre principali: una finestra per salvare i pezzi e una finestra per caricare i pezzi.

Per utilizzare la Macro copiare il contenuto del repository all'interno della cartella macro di freecad.

Per salvare i pezzi è necessario avere un disegno 3D aperto e un solido selezionato, avviare la macro "salva_pezzo" per aprire la finestra in cui è possibile registrare i parametri di salvataggio del pezzo selezionato.


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
    - ~~file linkato nel database non esistente~~
    - ~~lista clienti vuota~~
    - ~~lista materiali vuota~~
    - ~~file di configurazione mancante o vuoto e illegibile~~
    - percorso di salvataggio disegni non raggiungibile
    - permessi insufficienti percorso di salvataggio
    - ~~permessi insufficienti database~~ (non necessario)
