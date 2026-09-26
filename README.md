# Modulo 3 · Lezione 12 — Lab: l'assistente sui propri dati · guida agli script

Un laboratorio per obiettivi: due file con solo gli import, il codice lo scrive e
lo organizza ognuno. Qui c'è quello che serve per partire, i due temi di
riserva e la versione del docente.

## Prima di entrare in aula (docente)

1. **Ambiente.**

   ```bash
   cd scripts
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

   Poi il `.env` con la chiave.
2. **La versione del docente sul tema Valtesa**, che serve ai rientri:

   ```bash
   python solutions/obiettivo2_documenti.py     # collection «valtesa», meno di un centesimo
   python scaffolding/tabelle_in_db.py temi/valtesa/tabelle temi/valtesa/valtesa.db
   ```

   Una prova della chat: `python solutions/obiettivo4_assistente.py` con
   due o tre domande di `solutions/griglia.md`. Il file è senza correzioni
   (la colonna «Prima» della griglia): le due della griglia, la riga sui nomi
   uguali nelle istruzioni e `K = 8`, si fanno a lezione, dal vivo.
3. `python scaffolding/check_lab12.py --live`: tutto `[OK]`.
4. **`temi-docente.md`** (nella cartella della lezione, fuori da
   `scripts/`) ha, per i due temi:
   - le domande di prova con le risposte vere;
   - come sono andate su tre giri;
   - le trappole che scattano.

   Serve per chi si blocca: non è la consegna.

## I file

| File | Ruolo | Cosa fa |
|---|---|---|
| `CONSEGNA.md` | 📄 | setup, tema, formati, i cinque obiettivi con il «fatto quando», la strada corta |
| `MAPPA.md` | 📄 | i file e, per ogni obiettivo, le lezioni da riaprire e i pezzi di `aikit/` già scritti |
| `working/agente.py` | ⌨️ | solo il prologo e gli import: l'agente (obiettivi 1, 3 e 4) |
| `working/documenti.py` | ⌨️ | solo il prologo e gli import: il vector DB (obiettivo 2) |
| `working/griglia.md` | ⌨️ | le otto domande, prima e dopo la cura (obiettivo 5) |
| `dati/` | 📄 | vuota: `dati/documenti/` e `dati/tabelle/` le crea chi porta i propri file |
| `temi/valtesa/` | 📄 | tema di riserva: 6 documenti (PDF, DOCX, HTML, MD) e 3 tabelle CSV dell'ufficio del personale di Valtesa S.r.l. |
| `temi/valdoria/` | 📄 | tema di riserva: 6 documenti e 3 tabelle della Biblioteca civica di Valdoria |
| `scaffolding/aikit/` | 🧰 | il toolkit del corso, uguale alla lezione scorsa |
| `scaffolding/tabelle_in_db.py` | 🧰 | le tabelle CSV o Excel di una cartella in un database SQLite, una tabella per file (obiettivo 4): si lancia o se ne copiano le righe |
| `scaffolding/sql.py` | 🧰 | una query a mano su un database qualsiasi: `python scaffolding/sql.py temi/valtesa/valtesa.db "SELECT …"`; senza query stampa lo schema |
| `scaffolding/make_temi.py`, `tema_valtesa.py`, `tema_valdoria.py` | 🧰 | generano i due temi (i file sono già versionati); le trappole sono nei docstring. Richiede `reportlab` |
| `scaffolding/check_lab12.py` | 🧰 | il check del docente: struttura, temi, versione del docente; `--live` con chiamate vere |
| `solutions/obiettivo1_chat.py` | 🎤 | versione del docente, obiettivo 1: l'agente in chat con la sessione su file |
| `solutions/obiettivo2_documenti.py` | 🎤 | obiettivo 2: i documenti nella collection |
| `solutions/obiettivo3_agente_documenti.py` | 🎤 | obiettivo 3: l'agente con `cerca_documenti`, la traccia e la strada |
| `solutions/obiettivo4_assistente.py` | 🎤 | obiettivo 4: l'agente dell'obiettivo 3 con anche `query_db` |
| `solutions/griglia.md` | 🎤 | obiettivo 5: la griglia del docente su Valtesa, con la cura |

`solutions/` non ha gli stessi file di `working/`: in `working/` ci sono solo
due file con gli import, e la versione del docente è divisa per obiettivo (eccezione dichiarata nel
piano). Si mostra nei rientri, dopo le soluzioni di due o tre studenti.

## Diagnosi rapida in aula

Si guarda il «fatto quando» dell'obiettivo sul terminale dello studente.

| Cosa vedi | Cosa controllare |
|---|---|
| `InvalidArgumentError: … Expected a name containing 3-512 characters` | il nome della collection: niente spazi né accenti, almeno 3 caratteri, inizio e fine con una lettera o un numero |
| la risposta è in una tabella di un DOCX e l'agente non la trova | il loader DOCX di `aikit` legge solo i paragrafi: le tabelle di Word restano fuori dall'indice (`python-docx` le espone in `documento.tables`) |
| la collection ha 0 chunk | il ciclo legge solo i `.txt` (è `indicizza()` di `aikit/rag.py` copiata senza cambiare il `glob`), o la cartella è sbagliata |
| `ValueError: Formato non supportato` | un file con un'estensione che i loader non leggono (`.xlsx`, `.odt`, file nascosti): va tolto dalla cartella o saltato |
| `ValueError: Formato non supportato:` (estensione vuota) | c'è un file nascosto nella cartella (`.DS_Store` del Mac): il ciclo deve saltare i file con un'estensione che i loader non leggono |
| una tabella con una colonna sola (`id;nome;importo`) | il CSV viene da Excel in italiano, col punto e virgola: si usa il file `.xlsx` così com'è |
| una SELECT con `>` o `SUM` dà numeri strani, o `38,50` resta testo | virgola decimale in un CSV: di nuovo, il file `.xlsx` |
| le date non si confrontano | nel CSV sono `15/07/2026`: in SQLite le date si confrontano solo scritte `2026-07-15` (dal `.xlsx` lo script le scrive così) |
| una colonna con spazi o accenti nel nome («voce spesa») | nella query va tra virgolette doppie: `SELECT "voce spesa" FROM …` |
| `ModuleNotFoundError: No module named 'openpyxl'` | `pip install -r requirements.txt` di questa lezione (c'è `openpyxl` in più) |
| l'agente dice che il dato non è disponibile, e nella traccia c'è `relative path can't be expressed as a file URI` | `tools.DB` è un percorso relativo: va costruito da `SCRIPTS` (`SCRIPTS / "dati" / "tabelle.db"`) |
| `ModuleNotFoundError: No module named 'aikit'` | il file è fuori da `working/`, o ha un prologo diverso da quello di `agente.py` e `documenti.py` |
| l'agente risponde sui dati senza chiamare `query_db` | la descrizione del tool non ha tabelle e colonne, o le istruzioni non dicono quando usarlo |
| la traccia non si vede | manca la stampa dei `ToolCallItem` (è in `assistente_sdk.py` di Modulo 3 · Lezione 11) |
| dopo il riavvio l'agente non ricorda | la sessione non ha il file, o il nome è diverso (come nella lezione scorsa) |
