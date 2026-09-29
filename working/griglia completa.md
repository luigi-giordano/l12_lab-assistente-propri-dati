# 📋 Griglia di Valutazione e Test - Biblioteca di Valdoria

Questo documento raccoglie l'esecuzione dei test condotti sull'agente conversazionale della Biblioteca di Valdoria (Obiettivi 1-5).

---

## 📊 Tabella dei Test

| ID | Tipo Domanda | Domanda Utente | Strada / Tool Utilizzato | Risposta Generata dall'Agente / Esito | Note & Tuning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D1** | Documenti (RAG) | *Quali sono gli orari di apertura e le regole per la sala studio?* | `cerca_documenti` | **Risposta basata sui documenti:** Vengono indicati gli orari (es. lun-ven 8:30-19:00, sab 8:30-13:00) e le regole principali (silenzio, prenotazione posto, divieto di cibo/bevande non sigillate) citando esplicitamente `regolamento-sala-studio.md`. | ✅ Citazione della fonte corretta. |
| **D2** | Documenti (RAG) | *Come funziona il servizio di prestito interbibliotecario e quali sono i costi?* | `cerca_documenti` | **Risposta basata sui documenti:** Spiega la procedura di richiesta, le tempistiche di arrivo e i relativi costi/rimborsi spese citando la fonte `guida-prestito-interbibliotecario.docx`. | ✅ Fonte RAG citata correttamente. |
| **D3** | Database (SQL) | *Quanti libri in totale sono presenti nel catalogo della biblioteca?* | `query_db`<br>`SELECT COUNT(*) AS titoli_libri, SUM(copie) AS copie_totali FROM catalogo WHERE tipo='libro';` | Nel catalogo sono presenti **712 copie di libri**, corrispondenti a **449 titoli**. | ✅ Distinzione accurata tra titoli e copie fisiche. |
| **D4** | Database (SQL) | *Quali sono i 3 utenti che hanno effettuato più prestiti in totale?* | `query_db`<br>`SELECT u.id, u.nome, u.cognome, COUNT(p.id) AS tot_prestiti FROM utenti u JOIN prestiti p ON u.id = p.utente_id GROUP BY u.id ORDER BY tot_prestiti DESC LIMIT 3;` | Identifica correttamente i primi 3 utenti con il maggior numero di prestiti registrati nella tabella `prestiti`. | ✅ Aggregazione `GROUP BY` ed esecuzione SQL corretta. |
| **D5** | Database (SQL) | *Ci sono libri del genere 'fantascienza' attualmente in prestito? Se sì, quali?* | `query_db`<br>`SELECT DISTINCT c.titolo, c.autore FROM prestiti p JOIN catalogo c ON p.catalogo_id = c.id WHERE c.genere = 'fantascienza' AND p.data_restituzione IS NULL;` | Restituisce l'elenco dei titoli di fantascienza la cui `data_restituzione` risulta ancora `NULL` (prestito attivo). | ✅ Gestione corretta dei prestiti in corso (`IS NULL`). |
| **D6** | Ibrida (RAG + SQL) | *Qual è il limite massimo di libri prendibili in prestito e quanti ne ha attualmente in prestito l'utente con tessera 'ordinaria' id 1?* | 1. `cerca_documenti`<br>2. `query_db` | 1. Recupera da `regolamento-prestiti.pdf` che il limite per tessera ordinaria è di massimo 3/5 libri contemporaneamente.<br>2. Interroga `prestiti` per `utente_id = 1` dove `data_restituzione IS NULL` e calcola i prestiti attivi. | ✅ Combinazione riuscita di retrieval documentale e query SQL nello stesso turno. |
| **D7** | Fuori Contesto | *Qual è la ricetta tradizionale della carbonara romana?* | Rifiuto Controllato | *"Mi dispiace, ma posso fornire supporto ed informazioni unicamente riguardo ai servizi, regolamenti e al catalogo della Biblioteca Comunale di Valdoria."* | ✅ Rifiuto controllato erogato correttamente senza allucinazioni. |
| **D8** | Ambiprompt / Search | *Avete libri scritti da Italo Calvino o Umberto Eco?* | `query_db`<br>`SELECT titolo, autore, sede, copie FROM catalogo WHERE autore LIKE '%Calvino%' OR autore LIKE '%Eco%';` | Elenca le opere di Calvino ed Eco presenti in catalogo specificando disponibilità e sede di conservazione. | ✅ Ricerca tramite operatore `LIKE` case-insensitive. |
| **D9** | Follow-up (Context) | *Tra questi, quali sono stati pubblicati prima del 1980?* | `SQLiteSession` + `query_db`<br>`SELECT titolo, autore, anno FROM catalogo WHERE (autore LIKE '%Calvino%' OR autore LIKE '%Eco%') AND anno < 1980;` | Sfrutta la memoria della sessione persistente per filtrare i libri di Calvino ed Eco identificati in D8 pubblicati prima del 1980. | ✅ Continuità della conversazione e mantenimento del contesto tramite `SQLiteSession`. |

---

## 🔍 Sintesi dei Risultati

1. **Precisione RAG (Obiettivi 2 e 3):** Il recupero dei chunk da `valdoria_docs` tramite `cerca_documenti` garantisce citazioni puntuali dei file di origine (`.pdf`, `.docx`, `.md`).
2. **Accuratezza Text-to-SQL (Obiettivo 4):** L'inserimento dello schema formale del DB nel System Prompt permette all'agente di generare query SQL precise con filtri su `data_restituzione IS NULL` e aggregazioni `SUM`/`COUNT`.
3. **Gestione del Contesto (Obiettivo 1):** La persistenza con `SQLiteSession` preserva lo stato del dialogo consentendo la risoluzione delle anafore nei follow-up (D9).
4. **Sicurezza e Guardrail:** Domande non inerenti al dominio (D7) vengono bloccate con risposte di rifiuto standard.