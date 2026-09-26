# Modulo 3 · Lezione 12, consegna

Oggi costruisci da zero un assistente su un tema tuo: documenti e, se il
tema le ha, tabelle. In `working/` ci sono due file con solo gli import:
`agente.py` (obiettivi 1, 3 e 4) e `documenti.py` (obiettivo 2). Il resto lo
scrivi tu. I percorsi costruiscili da `SCRIPTS`, la cartella `scripts/`
(per esempio `SCRIPTS / "dati" / "documenti"`). Per ogni obiettivo c'è un
«fatto quando» e le lezioni da riaprire (sono in `MAPPA.md`).

## Setup (5')

```bash
cd scripts
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../../l11_agents-sdk-sessioni/scripts/.env .env
```

Su Windows il venv si crea con `python -m venv .venv`, e la copia della
chiave è `copy ..\..\l11_agents-sdk-sessioni\scripts\.env .env`. Le
dipendenze sono quelle della lezione scorsa, più `openpyxl` per i file
Excel.

## Il tema

- **I tuoi dati**: i documenti in `dati/documenti/`, le tabelle (se ci sono)
  in `dati/tabelle/`.
- **Oppure un tema di riserva**, già pronto:
  - `temi/valtesa/`: l'ufficio del personale di un'azienda;
  - `temi/valdoria/`: una biblioteca civica.

**Formati.**

- Documenti `.txt`, `.md`, `.pdf`, `.docx`, `.html`, fino a una ventina.
- Tabelle in CSV (virgola tra le colonne, punto nei decimali) o in Excel
  (`.xlsx`, il primo foglio), una per file. Se i dati sono in Excel, usa il
  file `.xlsx` così com'è.

## Gli obiettivi

**1. Un agente in chat, con la sessione (20').**
Fatto quando, chiusa e riaperta la chat con lo stesso nome, l'agente
ricorda lo scambio prima.

**2. Un vector DB con i tuoi documenti (45').**
Fatto quando una ricerca sulla collection restituisce chunk dei tuoi file,
con il nome del file.

**3. L'agente con i documenti (25').**
L'agente dell'obiettivo 1 con il tool `cerca_documenti` sulla collection
dell'obiettivo 2. Fatto quando:

- una domanda sui documenti cita un chunk;
- una domanda fuori tema viene rifiutata senza tool (si vede nella
  traccia).

**4. Il database SQL e il suo tool, se il tema ha tabelle (40').**
Le tabelle nel database le mette un file già pronto, per CSV ed Excel:

```bash
python scaffolding/tabelle_in_db.py dati/tabelle dati/tabelle.db
```

(con un tema di riserva: `temi/valtesa/tabelle temi/valtesa/valtesa.db`).
Puoi anche copiarne le righe in un tuo file. Poi all'agente il tool
`query_db`, con le tue tabelle e colonne nella descrizione. Fatto quando:

- una SELECT scritta a mano restituisce le righe giuste;
- una domanda sui dati dà il numero che la tua SELECT a mano conferma;
- una domanda che ha bisogno di tutte e due le fonti chiama i due tool.

Se il tema non ha tabelle, passa all'obiettivo 5.

**5. Provarlo e sistemarlo (45').**
Fatto quando `working/griglia.md` ha le tue otto domande, ognuna con:

- la risposta vera, cercata prima di lanciarla;
- la strada presa;
- l'esito.

Le otto domande sono tre sui documenti, tre sui dati, una che ha bisogno di
tutte e due le fonti, una senza risposta; più un follow-up su una di queste.
Se il tema non ha tabelle: sette sui documenti e una senza risposta.
Lancia ogni domanda almeno due volte: la stessa domanda non dà sempre la
stessa risposta. Ogni lancio in una sessione nuova, con un nome nuovo:
nella stessa sessione il modello vede la sua risposta di prima. Il follow-up
va nella sessione della domanda a cui si riferisce. Almeno una domanda sbagliata va sistemata senza romperne
altre, cambiando una cosa alla volta: dopo la modifica si rilanciano tutte.

## Se resti indietro

Prendi la strada corta, poi passa all'obiettivo dopo:

- **Obiettivo 1.** In `solutions/assistente_sdk.py` di Modulo 3 · Lezione
  11 (nel branch `soluzioni` della repo del corso) ci sono `apri_sessione()`
  e il ciclo della chat: copiali in `working/agente.py`, con un `Agent`
  senza tool e le istruzioni del tuo tema.
- **Obiettivo 2.** Copia in `working/documenti.py` `indicizza()` di `aikit/rag.py` e
  cambia `glob("*.txt")` in `iterdir()`: così com'è legge solo i `.txt`. Poi
  metti la tua cartella e il nome della collection nel `CONFIG`.
- **Obiettivo 3.** Copia `cerca_documenti` dallo stesso file di Modulo 3 ·
  Lezione 11 e riscrivi la sua descrizione e le istruzioni per il tuo tema:
  oggi parlano di Lumen. Cerca con `rag.recupera()`, che legge il nome della
  collection da `rag.CONFIG`: prima, `rag.CONFIG["collection"] = "<la tua
  collection>"`.
- **Obiettivo 4.** Per il tool, `aikit/tools.py` ha `query_db`: assegna a
  `tools.DB` il percorso del tuo database costruito da `SCRIPTS`
  (`SCRIPTS / "dati" / "tabelle.db"`) e, nella descrizione del tool,
  scrivi le tue tabelle e colonne al posto di quelle di Lumen.

Se sei bloccato, il docente riapre con te la lezione di riferimento.
