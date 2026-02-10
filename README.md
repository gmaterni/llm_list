# LLM Model Manager & Tester

Questa applicazione è un set di strumenti per gestire, filtrare e testare modelli di linguaggio (LLM) da diversi provider. Permette di mantenere una lista aggiornata di modelli funzionanti e delle loro capacità (come la dimensione della finestra di contesto).

## Funzionalità Principali

1.  **Recupero Modelli**: Script dedicati per ogni provider che interrogano le API ufficiali per ottenere la lista aggiornata dei modelli disponibili.
2.  **Filtraggio e Metadata**: Estrazione di informazioni cruciali come l'ID del modello e il limite di token in input (window size).
3.  **Validazione (Testing)**: Uno script di test automatizzato che verifica l'effettiva disponibilità dei modelli effettuando chiamate di test.
4.  **Organizzazione dei Dati**: Archiviazione strutturata dei modelli in file di testo, separando i modelli generali da quelli verificati come funzionanti.
5.  **Interfaccia Unificata**: Una classe `LlmProvider` per caricare facilmente le configurazioni e inizializzare i client dei diversi provider.

## Struttura del Progetto

### Script di Recupero (`models_<provider>.py`)
Ogni file `models_<name>.py` è responsabile del recupero dei modelli da un provider specifico:
- `models_gemini.py`
- `models_groq.py`
- `models_mistral.py`
- `models_cerebras.py`
- `models_openrouter.py`
- `models_huggingface.py`

Questi script generano tre tipi di file nella directory `data/`:
- `models_<provider>.txt`: Lista semplice degli ID dei modelli.
- `models_<provider>_wnd.txt`: Mappatura ID modello | Window Size (es. `gemini-1.5-pro|1024k`).
- `models_<provider>_info.txt`: Informazioni dettagliate in formato leggibile.

### Script di Test (`models_test.py`)
Esegue un test di connettività per ogni modello elencato nei file `data/models_<provider>.txt`.
- Verifica la validità delle chiavi API (lette dalle variabili d'ambiente).
- Salva i modelli che superano il test in `data/ok/<provider>.txt`.

### Gestore Provider (`llm_provider.py`)
Fornisce la classe `LlmProvider` che:
- Carica le chiavi API da `api_keys.json` (se presente) o variabili d'ambiente.
- Carica le configurazioni dei modelli dai file `_wnd.txt` in `data/`.
- Inizializza i client corrispondenti (utilizzando la libreria `llmclient`).

## Directory dei Dati
- `data/`: Contiene i file generati dagli script di recupero.
- `data/ok/`: Contiene le liste dei modelli verificati con successo dallo script di test.

## Utilizzo

1.  **Recupero**: Esegui uno degli script `models_<provider>.py` per aggiornare la lista dei modelli.
    ```bash
    python3 models_gemini.py
    ```
2.  **Test**: Esegui lo script di test per verificare quali modelli sono accessibili.
    ```bash
    python3 models_test.py
    ```
3.  **Integrazione**: Usa `llm_provider.py` nel tuo codice per accedere ai modelli configurati.

## Requisiti
- Python 3.x
- Librerie: `requests`, `google-genai` (per Gemini), e i client specifici definiti in `llmclient`.
- Chiavi API configurate come variabili d'ambiente (es. `GEMINI_API_KEY`, `GROQ_API_KEY`, ecc.).
