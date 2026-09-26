# Mappa della lezione

## I file

| File | Cosa è |
|---|---|
| `working/agente.py` | solo gli import: qui scrivi l'agente (obiettivi 1, 3 e 4) |
| `working/documenti.py` | solo gli import: qui scrivi il vector DB (obiettivo 2) |
| `working/griglia.md` | le tue otto domande, prima e dopo la cura (obiettivo 5) |
| `dati/` | vuota: qui i tuoi documenti (`dati/documenti/`) e le tue tabelle (`dati/tabelle/`) |
| `temi/valtesa/` | tema di riserva: l'ufficio del personale di Valtesa S.r.l. (6 documenti, 3 tabelle) |
| `temi/valdoria/` | tema di riserva: la Biblioteca civica di Valdoria (6 documenti, 3 tabelle) |
| `scaffolding/aikit/` | il toolkit del corso, come nella lezione scorsa: si importa, non si modifica |
| `scaffolding/tabelle_in_db.py` | le tabelle CSV o Excel di una cartella in un database: `python scaffolding/tabelle_in_db.py dati/tabelle dati/tabelle.db` |
| `scaffolding/sql.py` | una query a mano su un database: `python scaffolding/sql.py percorso.db "SELECT …"` |
| `CONSEGNA.md` | setup, tema, obiettivi |

Il resto (`scaffolding/make_temi.py`, `tema_*.py`, `check_lab12.py`,
`solutions/`) è del docente.

## Obiettivo per obiettivo

Le lezioni sono nella repo del corso: `modulo2-llm-data/` e `modulo3-rag/`.

| Obiettivo | Da riaprire | Già scritto in `aikit/` |
|---|---|---|
| 1. Agente in chat | Modulo 3 · Lezione 10 (`l10_agents-sdk-loop-gestito`): `Agent`, `Runner`; Modulo 3 · Lezione 11 (`l11_agents-sdk-sessioni`): la sessione su file, la chat | `apri_sessione()` e il ciclo della chat sono in `assistente_sdk.py` di Modulo 3 · Lezione 11 |
| 2. Vector DB | Modulo 2 · Lezione 4 (`l04_data-loading`), 5 (`l05_text-cleaning`), 7 (`l07_embeddings`), 9 (`l09_vector-databases`), 10 (`l10_chunking-strategies`); Modulo 3 · Lezione 2 (`l02_rag-end-to-end`) | `loaders.load`, `clean.clean` e `pipeline_for`, `chunk.chunk_recursive`, `embeddings.embed`, `vectorstore` (`crea_collection`, `indicizza`, `search`); `rag.indicizza` e `rag.recupera` |
| 3. Agente con i documenti | Modulo 3 · Lezione 7 (`l07_tool-calling-intro`): cosa vede il modello di un tool; Lezione 9 (`l09_lab-rag-tools`): il RAG come tool, le istruzioni, il rifiuto; Lezione 11: `assistente_sdk.py` | `cerca_documenti`, `ISTRUZIONI` e `strada()` sono in `assistente_sdk.py` di Modulo 3 · Lezione 11 |
| 4. Database SQL e `query_db` (se il tema ha tabelle) | Modulo 3 · Lezione 8 (`l08_tool-implementation`): `query_db` e lo schema nella descrizione | `scaffolding/tabelle_in_db.py` (le tabelle nel database); `tools.query_db` (legge `tools.DB`) |
| 5. Provarlo e sistemarlo | Modulo 3 · Lezione 6 (`l06_lab-rag-debugging`): la risposta attesa, una leva alla volta; Lezione 9: strade ed esiti in griglia | — |
