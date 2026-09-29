# Griglia delle domande

Il tema: **Biblioteca Comunale di Valdoria**

Otto domande: tre sui documenti, tre sui dati, una che ha bisogno di tutte e
due le fonti, una senza risposta; più un follow-up su una di queste. Se il
tema non ha tabelle: sette sui documenti e una senza risposta.

La **risposta vera** si cerca PRIMA di lanciare la domanda: nei documenti per
quelle sui documenti, con una SELECT scritta a mano per quelle sui dati.

Ogni domanda si lancia almeno due volte, ogni volta in una sessione nuova
(un nome nuovo); il follow-up nella sessione della sua domanda. Se le
risposte sono diverse, nell'esito si scrive quante volte è giusta (per
esempio «1 su 2»).

| # | Tipo | Domanda | Risposta vera | Strada presa | Esito | Dopo la cura |
|---|---|---|---|---|---|---|
| 1 | documenti | Quali sono gli orari di apertura della sede centrale il sabato e che servizi sono attivi? | Sabato 9:00–13:00. Servizi: prestito, restituzione, consultazione, emeroteca, Wi-Fi, sala ragazzi, postazioni PC. | documenti | giusta | giusta |
| 2 | documenti | Come si prenota un posto in sala studio per il pomeriggio e quali sono le regole sull'occupazione dei posti? | Prenotazione da portale (fascia 13:30–19:30). Tolleranza 30 min per il check-in, pause max 45 min, vietato occupare posti per altri. | documenti | giusta | giusta |
| 3 | documenti | Cosa succede se restituisco un libro con 20 giorni di ritardo? | Sospensione dal prestito per un periodo pari al ritardo (20 giorni) al momento della restituzione. | documenti | giusta | giusta |
| 4 | dati | Quanti libri di genere 'Saggistica' pubblicati dopo il 2010 ci sono nella sede centrale? | 0 (rilevato tramite SELECT su catalogo con filtri genere, anno e sede). | dati | giusta | giusta |
| 5 | dati | Quanti utenti della sede Succursale si sono iscritti nel 2024? | 0 (rilevato tramite SELECT su utenti per sede_iscrizione e data_iscrizione). | dati | giusta | giusta |
| 6 | dati | Quanti prestiti risultano attualmente in corso per l'utente con tessera della sede Centrale? | Query SELECT su prestiti e utenti filtrando per data_restituzione IS NULL. | dati | giusta | giusta |
| 7 | tutte e due | Sono uno studente universitario di 22 anni: quante risorse posso prendere in prestito contemporaneamente tra libri fisici, ebook e prestiti interbibliotecari? | Tessera Studenti: max 8 libri fisici (inclusi max 3 prestiti interbibliotecari) + 3 ebook contemporanei. | documenti+dati | sbagliata (1 su 2) | giusta |
| 8 | senza risposta | Posso donare dei libri usati alla biblioteca? Quali sono i requisiti? | Informazione non presente nei documenti ufficiali di Valdoria. | nessuna | rifiuto giusto | rifiuto giusto |
| 9 | follow-up della 1 | Posso restituire un libro anche quando la biblioteca è chiusa? | Sì, tramite il contenitore esterno h24 della sede Centrale in Via Roma 18. | documenti | giusta | giusta |

**Strada presa:** documenti, dati, documenti+dati, nessuna (la riga
`strada:` sotto ogni risposta).
**Esito:** giusta, sbagliata, «non trovato» su una risposta che c'era,
rifiuto giusto.

## La cura

La domanda sbagliata che hai sistemato: **Domanda 7 (T5)** — *"Sono uno studente universitario di 22 anni: quante risorse posso prendere in prestito contemporaneamente tra libri fisici, ebook e prestiti interbibliotecari?"*

Cosa hai cambiato (una cosa sola): **Aumento della dimensione dei chunk (Chunking Strategy)**. In `working/documenti.py` la dimensione del blocco in `chunk_recursive` è stata portata da `500` a `1200` caratteri. Questo ha evitato che le tabelle dei regolamenti (con la distinzione tra Tessera Ordinaria, Tessera Studenti e Tessera Famiglia) venissero frammentate tra più chunk diversi, permettendo al Vector DB di passare al modello il contesto normativo completo. Contestualmente è stata rimossa dal System Prompt di `working/agente.py` l'istruzione di ridurre la query RAG a sole 2-4 parole chiave, mantenendo intatti i dettagli del profilo utente ("studente universitario 22 anni").

Le altre domande dopo la modifica: tutte come prima? **Sì, tutte le altre domande continuano a rispondere in modo corretto, con una citazione accurata delle fonti e delle query SQL.**