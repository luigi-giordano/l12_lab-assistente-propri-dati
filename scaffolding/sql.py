"""sql.py — una query a mano su un database SQLite, senza modello.

Strumento di servizio: serve a guardare i dati e a cercare la risposta vera
prima di fare la domanda all'agente. Connessione in sola lettura, una query
per lancio, il risultato a schermo. Senza query stampa lo schema.

Uso (dalla cartella scripts/):
    python scaffolding/sql.py temi/valtesa/valtesa.db
    python scaffolding/sql.py temi/valtesa/valtesa.db "SELECT * FROM dipendenti LIMIT 5"
"""
import sqlite3
import sys
from pathlib import Path



def stampa_schema(con):
    tabelle = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY rowid")]
    for tabella in tabelle:
        n = con.execute(f"SELECT COUNT(*) FROM {tabella}").fetchone()[0]
        colonne = [f"{c[1]} {c[2]}" for c in con.execute(f"PRAGMA table_info({tabella})")]
        print(f"{tabella} ({n} righe)\n    " + ", ".join(colonne))


def stampa_tabella(colonne, righe):
    righe = [["" if v is None else str(v) for v in r] for r in righe]
    larghezze = [max(len(c), *(len(r[i]) for r in righe)) if righe else len(c) for i, c in enumerate(colonne)]
    print("  ".join(c.ljust(larghezze[i]) for i, c in enumerate(colonne)))
    print("  ".join("-" * l for l in larghezze))
    for r in righe:
        print("  ".join(v.ljust(larghezze[i]) for i, v in enumerate(r)))
    print(f"({len(righe)} righe)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Uso: python scaffolding/sql.py percorso.db ["SELECT …"]')
    db = Path(sys.argv[1])
    if not db.exists():
        raise SystemExit(f"Il file {db} non esiste")
    con = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True)   # as_uri: regge cartelle con # o spazi
    if len(sys.argv) < 3:
        stampa_schema(con)
    else:
        try:
            cur = con.execute(sys.argv[2])
            stampa_tabella([d[0] for d in cur.description], cur.fetchall())
        except Exception as e:                    # una query sbagliata: il messaggio, senza traceback
            print(f"Errore: {e}")
    con.close()
