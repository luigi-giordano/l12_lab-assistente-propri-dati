"""agente.py — l'agente del tuo tema: la chat con la sessione (obiettivo 1),
poi il tool cerca_documenti (obiettivo 3) e il tool query_db (obiettivo 4).

Qui ci sono solo il prologo e gli import: il resto lo scrivi tu.

Uso (dalla cartella scripts/):  python working/agente.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent              # la cartella scripts/: i percorsi si costruiscono da qui
sys.path.insert(0, str(SCRIPTS / "scaffolding"))    # per importare aikit

from dotenv import load_dotenv
load_dotenv(SCRIPTS / ".env")                       # la chiave, prima di importare agents

from agents import Agent, Runner, function_tool, SQLiteSession, MaxTurnsExceeded, ToolCallItem
from aikit import rag, tools                        # rag.recupera per cerca_documenti, tools.query_db per query_db
