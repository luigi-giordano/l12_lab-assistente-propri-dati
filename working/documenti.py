"""
documenti.py — Ingestion e indicizzazione dei documenti del tema Valdoria (Obiettivo 2).

Uso (dalla cartella principale del laboratorio):
    python working/documenti.py
"""

import sys
from pathlib import Path

# Configurazione dei percorsi di sistema per importare i moduli di scaffolding e aikit
SCRIPTS = Path(__file__).parent.parent  # La radice del progetto
sys.path.insert(
    0, str(SCRIPTS / "scaffolding")
)  # Aggiunge scaffolding al path di Python

from dotenv import load_dotenv

load_dotenv(SCRIPTS / ".env")  # Carica le variabili d'ambiente (OPENAI_API_KEY)

# Import dei moduli nativi forniti da aikit
from aikit.loaders import load  # Caricamento multiformato (pdf, docx, html, md)
from aikit.chunk import chunk_recursive  # Chunking del testo
from aikit.embeddings import embed  # Modulo per la generazione degli embedding
from aikit import vectorstore  # Gestione del Vector DB

try:
    from aikit.clean import clean, pipeline_for

    HAS_CLEAN = True
except ImportError:
    HAS_CLEAN = False

# Definizione dei percorsi per i documenti e per il vector database di Valdoria
DIR_DOCUMENTI = SCRIPTS / "temi" / "valdoria" / "documenti"
NOME_COLLEZIONE = "valdoria_docs"


def estrai_testo_documento(doc) -> str:
    """
    Funzione di supporto per estrarre il testo da un oggetto restituito dai loader di aikit.
    """
    if isinstance(doc, str):
        return doc
    if hasattr(doc, "text"):
        return doc.text
    if hasattr(doc, "page_content"):
        return doc.page_content
    if isinstance(doc, dict):
        return doc.get("text") or doc.get("content") or ""
    return str(doc)


def pulisci_testo(testo: str) -> str:
    """
    Pulisce il testo rimuovendo spazi doppi o righe vuote eccessive.
    """
    if not testo:
        return ""

    if HAS_CLEAN:
        try:
            pipe = pipeline_for("text")
            return pipe(testo)
        except Exception:
            try:
                return clean(testo, steps=["whitespace"])
            except Exception:
                pass

    return " ".join(testo.split())


def dividi_in_chunk(testo: str, dimensione: int = 500):
    """
    Richiama chunk_recursive passando i 2 argomenti richiesti da aikit (testo, dimensione).
    """
    try:
        return chunk_recursive(testo, dimensione)
    except TypeError:
        return chunk_recursive(testo, size=dimensione)


def costruisci_vectorstore():
    """
    Legge tutti i documenti della cartella, li pulisce, li suddivide in chunk,
    calcola gli embedding e li salva nel Vector Database locale con aikit.
    """
    print("🚀 Inizio processo di ingestion per il tema Valdoria...")

    file_documenti = list(DIR_DOCUMENTI.glob("*.*"))
    if not file_documenti:
        print(f"❌ Nessun file trovato nella cartella: {DIR_DOCUMENTI}")
        return

    print(f"📂 Trovati {len(file_documenti)} file nella cartella documenti.")

    tutti_i_chunk = []
    tutti_i_metadati = []

    # Iteriamo su ciascun documento per effettuarne il caricamento, la pulizia e il chunking
    for file_path in file_documenti:
        print(f"\n📖 Elaborazione: {file_path.name}")

        try:
            docs = load(str(file_path))

            if not isinstance(docs, list):
                docs = [docs]

            for doc in docs:
                testo_grezzo = estrai_testo_documento(doc)

                if not testo_grezzo.strip():
                    continue

                testo_pulito = pulisci_testo(testo_grezzo)
                chunks_doc = dividi_in_chunk(testo_pulito, dimensione=500)

                for c in chunks_doc:
                    testo_c = c if isinstance(c, str) else estrai_testo_documento(c)
                    if testo_c.strip():
                        tutti_i_chunk.append(testo_c)
                        tutti_i_metadati.append({"source": file_path.name})

            print(f"   └─ Estratti e preparati i chunk per: {file_path.name}")

        except Exception as e:
            print(f"❌ Errore durante l'elaborazione del file {file_path.name}: {e}")

    print(f"\n🧩 Totale chunk preparati: {len(tutti_i_chunk)}")

    if not tutti_i_chunk:
        print("❌ Nessun chunk valido estratto. Impossibile creare il vectorstore.")
        return

    # 1. Creazione degli ID univoci per ogni chunk
    ids = [f"valdoria-chunk-{i}" for i in range(len(tutti_i_chunk))]

    # 2. Generazione degli embedding tramite aikit
    print("🧠 Calcolo degli embedding per i chunk...")
    vettori_embedding = embed(tutti_i_chunk)

    # 3. Inizializzazione della collezione Chroma pulita
    print("💾 Creazione collezione e salvataggio nel Vector Store...")
    collection = vectorstore.crea_collection(NOME_COLLEZIONE)

    # 4. Indicizzazione esplicita dei dati
    vectorstore.indicizza(
        collection=collection,
        ids=ids,
        testi=tutti_i_chunk,
        embeddings=vettori_embedding,
        metadatas=tutti_i_metadati,
    )

    print(f"✅ Vector DB creato e indicizzato con successo in Chroma!")
    return collection


if __name__ == "__main__":
    costruisci_vectorstore()
