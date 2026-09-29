"""
agente.py — L'agente conversazionale per il tema Biblioteca di Valdoria.

In questo file implementiamo:
1. Obiettivo 1: La chat conversazionale con sessione persistente (SQLiteSession).
2. Obiettivo 3: Il tool RAG 'cerca_documenti' basato sulla ricerca vettoriale semantica.
3. Obiettivo 4: Il tool 'esegui_query_db' per interrogare il database relazionale SQLite.

Uso (dalla cartella radice del progetto):
    python working/agente.py
"""

import sys
import asyncio
import inspect
from pathlib import Path

# ==============================================================================
# PROCEDIMENTO 1: MAPPATURA DEI PERCORSI E CARICAMENTO DELL'AMBIENTE
# ==============================================================================
SCRIPTS = Path(__file__).parent.parent  # Cartella radice del laboratorio
sys.path.insert(
    0, str(SCRIPTS / "scaffolding")
)  # Inserisce scaffolding in testa ai moduli importabili

from dotenv import load_dotenv

load_dotenv(SCRIPTS / ".env")  # Carica la API Key di OpenAI dall'ambiente

from agents import (
    Agent,
    Runner,
    function_tool,
    SQLiteSession,
    MaxTurnsExceeded,
)
from aikit import rag, tools  # Modulo RAG (recupera) e utility per i tool

# ==============================================================================
# CONFIGURAZIONE COSTANTI E DATABASE
# ==============================================================================
NOME_COLLEZIONE = "valdoria_docs"  # Nome della collezione Chroma creata in documenti.py
DB_VALDORIA = (
    SCRIPTS / "temi" / "valdoria" / "valdoria.db"
).resolve()  # Database relazionale con le tabelle
tools.DB = DB_VALDORIA
DB_SESSIONI = (
    SCRIPTS / "temi" / "valdoria" / "sessioni.db"
)  # DB SQLite dove vengono salvati i messaggi
NOME_SESSIONE = "valdoria_user_session"  # ID unico per identificare la sessione utente


# ==============================================================================
# PROCEDIMENTO 2: DEFINIZIONE TOOL RAG 'cerca_documenti' (OBIETTIVO 3)
# ==============================================================================
@function_tool
def cerca_documenti(query: str, k: int = 3) -> str:
    """Cerca all'interno dei documenti e regolamenti non strutturati della Biblioteca di Valdoria."""
    print(f"\n🔍 [TOOL RAG] Cercando nei documenti: '{query}'")
    try:
        # Passiamo NOME_COLLEZIONE come primo parametro posizionale (senza collezione=...)
        risultati = rag.recupera(query, k)

        if not risultati:
            return "Nessun documento o regolamento pertinente trovato nei file di Valdoria."

        testi_formattati = []
        for idx, res in enumerate(risultati, start=1):
            if isinstance(res, dict):
                metadata = res.get("metadata", {})
                fonte = (
                    metadata.get("source")
                    or res.get("source")
                    or res.get("id")
                    or "Documento Sconosciuto"
                )
                testo = res.get("testo") or res.get("text") or res.get("document") or ""
                score = res.get("score", 0.0)
            else:
                fonte = getattr(res, "source", "Documento Sconosciuto")
                testo = getattr(res, "text", str(res))
                score = 0.0

            testi_formattati.append(
                f"--- CHUNK {idx} (Fonte: {fonte} | Rilevanza: {score:.2f}) ---\n{testo.strip()}"
            )

        return "\n\n".join(testi_formattati)

    except Exception as e:
        print(f"❌ [TOOL RAG ERROR]: {e}")
        return f"Errore durante il recupero dei documenti: {e}"


# ==============================================================================
# PROCEDIMENTO 3: DEFINIZIONE TOOL DATABASE 'esegui_query_db' (OBIETTIVO 4)
# ==============================================================================
@function_tool
def esegui_query_db(sql_query: str) -> str:
    """Esegue una query SQL di sola lettura (SELECT) sul database relazionale della biblioteca Valdoria.

    Args:
        sql_query: La query SQL SELECT valida da eseguire su valdoria.db.
    """
    print(f"\n⚙️ [TOOL EXECUTION] Eseguo query SQL: {sql_query}")
    try:
        risultato = tools.query_db(sql=sql_query)
        print(f"📊 [TOOL RESULT]: {risultato}\n")
        return str(risultato)
    except Exception as e:
        print(f"❌ [TOOL ERROR]: {e}\n")
        return f"Errore durante l'esecuzione della query SQL: {e}"


# ==============================================================================
# PROCEDIMENTO 4: PROMPT DI SISTEMA CON SCHEMA DB ED EROGAZIONE RIFIUTI CONTROLLATI
# ==============================================================================
SYSTEM_PROMPT = """Sei l'assistente virtuale ufficiale della Biblioteca Comunale di Valdoria.

Disponi di due strumenti (tool):
1. `esegui_query_db`: DEVI USARE QUESTO TOOL per qualsiasi domanda che richieda di contare, cercare o consultare i dati su LIBRI, CATALOGO, UTENTI e PRESTITI. Non inventare mai numeri e non dire che il database non è accessibile senza aver prima chiamato questo tool.
2. `cerca_documenti`: Usa questo tool per domande su regolamenti, orari, sale studio e carte dei servizi.

### SCHEMA DEL DATABASE RELAZIONALE (`valdoria.db`):
- `utenti` (id, nome, cognome, tessera, data_iscrizione, sede_iscrizione)
- `catalogo` (id, titolo, autore, genere, anno, sede, tipo, copie)  --> tipo può essere 'libro', 'dvd', 'rivista'
- `prestiti` (id, utente_id, catalogo_id, data_prestito, data_scadenza, data_restituzione, rinnovi)

### DIRETTIVE:
- Per contare i libri nel catalogo, esegui una query SQL del tipo: `SELECT COUNT(*), SUM(copie) FROM catalogo WHERE tipo='libro';`
- Se usufruisci dei documenti di testo, cita sempre la fonte (es. 'secondo il regolamento-prestiti.pdf...').
- Rifiuta gentilmente solo le domande del tutto estranee alla Biblioteca di Valdoria.
"""


# ==============================================================================
# PROCEDIMENTO 5: INIZIALIZZAZIONE AGENTE E CICLO REPL CON SESSIONE PERSISTENTE
# ==============================================================================
async def esegui_agente():
    """Inizializza l'agente e gestisce il ciclo REPL asincrono con sessione SQLite persistente."""

    sessione = SQLiteSession(session_id=NOME_SESSIONE, db_path=str(DB_SESSIONI))

    agente = Agent(
        name="Assistente Valdoria",
        instructions=SYSTEM_PROMPT,
        tools=[cerca_documenti, esegui_query_db],
    )

    print("🤖 Assistente Biblioteca Valdoria avviato (Obiettivi 1, 3 e 4 attivi).")
    print("Scrivi 'exit' o 'quit' per uscire.\n")

    while True:
        try:
            # Usiamo asyncio.to_thread per non bloccare l'event loop durante l'input dell'utente
            user_input = await asyncio.to_thread(input, "Utente > ")
            user_input = user_input.strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("👋 Arrivederci!")
                break

            # Esecuzione asincrona dell'agente nel medesimo Event Loop
            if inspect.iscoroutinefunction(Runner.run):
                risultato = await Runner.run(agente, input=user_input, session=sessione)
            else:
                risultato = Runner.run(agente, input=user_input, session=sessione)
                if inspect.iscoroutine(risultato):
                    risultato = await risultato

            # Estrazione dell'output
            if hasattr(risultato, "final_output"):
                testo_risposta = risultato.final_output
            else:
                testo_risposta = str(risultato)

            print(f"\nAssistente > {testo_risposta}\n")

        except MaxTurnsExceeded:
            print("\n⚠️ Raggiunto il limite massimo di passaggi per questo turno.\n")
        except KeyboardInterrupt:
            print("\n👋 Sessione interrotta.")
            break
        except Exception as e:
            print(f"\n❌ Errore durante l'esecuzione: {e}\n")


if __name__ == "__main__":
    # Avviamo un UNICO event loop per tutta la durata dell'applicazione
    asyncio.run(esegui_agente())
