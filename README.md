# interfaccia_parametri

## Obiettivo:

Finestra per la compilazione di dati da salvare su database.

## Installazione prerequisiti:


- Installare psycopg2 per connettersi al database postgres con il comando:
```shell
pip3 install psycopg2
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
- Scaricare Postgres per Docker:
```shell
docker pull postgres
```
- Avviare la prima volta il container Postgres:
```shell
docker run --name freeprof -e POSTGRES_PASSWORD=mypass -d -p 5432:5432 postgres
```
dove freeprof è il nome del container
- Per Avviare, fermare o riavviare il container Mariadb:
```shell
docker start postgres
```
```shell
docker stop postgres
```
```shell
docker restart postgres
```
- Il container Postgres non si avvia automaticamente all'avvio del sistema operativo. Per fare ciò usiamo crontab:
```shell
crontab -e
```
- selezioniamo l'editor preferito e aggiungiamo la seguente riga in fondo al file di testo appena aperto:
```text
@reboot docker start postgres
```
- Per accedere alla linea di comando del container:
```shell
docker exec -it postgres bash
```
- Per accedere direttamente al database nel container: 
```shell
docker exec -ti freeprof psql -d postgres -U postgres
```
- Creare un nuovo utente e all'interno di postgres: 
```sql
CREATE USER freecad WITH PASSWORD 'casualpass';
```
- Creare un database per la macro:
```sql
CREATE DATABASE freeprof OWNER freecad;
```
## Risorse utilizzate:

- Freecad 0.19: https://github.com/FreeCAD/FreeCAD/releases
- Docker: https://www.docker.com/
- GUI per Docker: https://github.com/docker/kitematic/releases 
- Esempi di codice Python per Postgres: https://www.postgresqltutorial.com/postgresql-python/connect/

## Istruzioni:

La Macro consiste in 2 finestre principali: una finestra per salvare i pezzi e una finestra per caricare i pezzi.

Per utilizzare la Macro, copiare il contenuto del repository all'interno della cartella macro di freecad.

#### File di configurazione:

All'interno della cartella "resources":
- aprire con un editor di testo il file "**macro_config.json**" e impostare il percorso della cartella di salvataggio desiderata. Tale percorso verrà utilizzato sia dalla macro di salvataggio. La macro di caricamento invece utilizzerà il percorso memorizzato all'interno del database.
- I file "**clienti.csv**", "**denominazione_profile.csv**" e "**materiali.csv**" possono essere modificati tramite editor di testo per aggiungere o rimuovere i valori desiderati.

All'interno della cartella "**resources/database**", aprire con un editor di testo il file "**db_config.json**" e impostare i parametri di accesso al database. (Non è necessario se il database è stato creato seguendo le istruzioni dei prerequisiti)

#### Uso delle macro:
Per salvare i pezzi è necessario avere un disegno 3D aperto e un solido selezionato, avviare la macro "**salva_pezzo.py**" per aprire la finestra in cui è possibile registrare i parametri di salvataggio del pezzo selezionato. Una volta compilato i campi nel modo desiderato, premere il pulsante salva che provvederà a creare una copia dell'elemento selezionato e lo salverà nel percorso selezionato.

Per caricare un pezzo, avviare la macro "**carica_pezzo.py**" e utilizzare i campi per interrogare il database. Selezionare il pezzo desiderato e premere carica.

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

~~Aggiungere salvataggio del file su percorso prestabilito, con creazione sottocartella in base al nome del cliente, quindi + proprietà di percorso file~~

~~Estrae immediatamente i dati e li immette nel database~~

~~Meglio gestire prima creazione e modifica con un unico tasto, quindi unica macro~~

## TODO list:

- Correggere bug sovrascrittura file esistenti
- ~~Funzione per modifica manuale dei pezzi dal database~~
- Funzione eliminazione manuale dei pezzi dal database
- ~~Creazione anteprima durante salvataggio pezzo~~
- ~~Visualizzazione anteprima durante caricamento pezzo~~

- ~~File di configurazione con percorso di salvataggio dei file~~
- ~~Funzione di estrazione dati da database~~
- ~~Maschera per la ricerca dei pezzi tramite database~~
- Funzione di riconoscimento revisioni vecchie da cancellare dal database (mantenere il file)
- ~~gestione suffisso delle parti e gestione dell'indice di revisione~~
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
