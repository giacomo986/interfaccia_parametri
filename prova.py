"""
CREATE TABLE IF NOT EXISTS parti (
    parte_id                integer PRIMARY KEY,
    riferimento             TEXT NOT NULL,
    codice_padre            TEXT NOT NULL,
    macchina                TEXT NOT NULL,
    materiale               TEXT NOT NULL,
    denominazione_profilo   TEXT NOT NULL,
    data_creazione          date NOT NULL,
    ultima_modifica         date NOT NULL,
    nome                    TEXT NOT NULL,
    codice                  TEXT NOT NULL,
    cliente                 TEXT NOT NULL,
    quantità_per_disegno    INT NOT NULL,
    misura_di_massima       FLOAT NOT NULL,
    massa                   FLOAT NOT NULL,
    percorso                TEXT NOT NULL
);
"""

