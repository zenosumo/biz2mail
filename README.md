
# biz2mail

## Descrizione
`biz2mail` è uno script Python progettato per elaborare file Excel contenenti dati aziendali e popolare le colonne "website" ed "email" utilizzando ricerche su DuckDuckGo e analisi del contenuto delle pagine web.

## Requisiti
- Python 3.x
- Librerie Python: pandas, requests, openpyxl, xlrd, re, urllib.parse, duckduckgo_search

Per installare le librerie necessarie, eseguire:
```bash
pip install pandas requests openpyxl xlrd duckduckgo_search
```

## Funzionalità
1. Genera un file CSV da un file Excel.
2. Popola le colonne "website" ed "email" in un file CSV.
3. Salva i record trovati con successo in un file separato con suffisso `-resolved`.

## Utilizzo

### Passo 1: Genera CSV da Excel
1. Esegui lo script:
    ```bash
    python biz2mail.py
    ```
2. Seleziona l'opzione "1" per generare il CSV da un file Excel.
3. Verrà richiesta la selezione di un file Excel dalla directory corrente. Scegli il file inserendo il numero corrispondente.
4. Specifica i nomi delle colonne per il Codice Fiscale e la Denominazione Azienda. Premere Invio per accettare i valori predefiniti.

Il CSV generato avrà le colonne "website", "email" e "error" vuote.

### Passo 2: Popola dati di "website" ed "email" nel CSV
1. Esegui lo script:
    ```bash
    python biz2mail.py
    ```
2. Seleziona l'opzione "2" per popolare le colonne "website" ed "email" nel CSV.
3. Verrà richiesta la selezione di un file CSV dalla directory corrente. Scegli il file inserendo il numero corrispondente. I file con suffisso `-resolved` saranno esclusi dalla lista.
4. Lo script elaborerà ogni record del CSV:
    - Se il campo "error" è valorizzato, il record sarà saltato.
    - Se il campo "website" è vuoto, verrà effettuata una ricerca su DuckDuckGo utilizzando il nome dell'azienda e il Codice Fiscale.
    - Se un sito web viene trovato, verrà popolato il campo "website".
    - Se il sito web è valido, verranno cercate le email nel sito e nel root del dominio.
    - Le email trovate verranno aggiunte al campo "email".
    - Se un timeout si verifica durante il recupero dell'URL, il campo "error" sarà impostato su "timeout".
    - Se vengono trovati sia il sito web che l'email, il record sarà aggiunto al file `-resolved` e l'errore sarà impostato su "no".

### File generati
- `filename.csv`: File CSV originale con i dati elaborati.
- `filename-resolved.csv`: File CSV contenente solo i record per cui sono stati trovati sia il sito web che l'email.

### Esempio di Esecuzione
```bash
python biz2mail.py
```

#### Output:
```
Scegli un'operazione da eseguire:
1: Genera CSV da Excel
2: Popola dati di "website" ed "email" nel CSV
Q: Esci
Inserisci la tua scelta (1/2/Q): 1
Seleziona un file Excel da usare:
1: aziende.xlsx
Q: Esci
Inserisci il numero del file da usare o Q per uscire: 1
Inserisci il nome della colonna per il Codice Fiscale [Codice Fiscale]: 
Inserisci il nome della colonna per la Denominazione Azienda [Denominazione Azienda]: 
CSV file created: aziende.csv
```

#### Popolazione di "website" ed "email":
```bash
python biz2mail.py
```

#### Output:
```
Scegli un'operazione da eseguire:
1: Genera CSV da Excel
2: Popola dati di "website" ed "email" nel CSV
Q: Esci
Inserisci la tua scelta (1/2/Q): 2
Seleziona un file CSV da usare:
1: aziende.csv
Q: Esci
Inserisci il numero del file da usare o Q per uscire: 1
Searching 1/100: Azienda ABC
...
CSV files updated: aziende.csv and aziende-resolved.csv
```

### Log
Un file di log (`biz2mail.log`) sarà creato nella directory corrente contenente i dettagli delle operazioni eseguite e gli eventuali errori riscontrati.

## Note
- Assicurarsi di avere una connessione internet attiva per eseguire le ricerche su DuckDuckGo.
- Lo script gestisce eventuali timeout e errori HTTP durante il recupero dei dati dai siti web.

## Contatti
Per qualsiasi domanda o problema, contattare [il tuo indirizzo email].
