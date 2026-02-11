# SYSTEM INSTRUCTIONS: GUIDA SVILUPPO GEMINI CLI

> **IMPORTANTE PER L'AGENTE:** Questo documento rappresenta la "Costituzione" del codice per questo progetto. Ogni riga di codice generata DEVE aderire a queste regole. Ignorare queste direttive è considerato un errore critico.

## FILOSOFIA DI FONDO
"Il codice è fondamentalmente un testo che descrive un processo secondo regole formali, destinato ad essere letto e compreso da altri programmatori. Solo in secondo luogo è un insieme di istruzioni eseguibili da una macchina".

## 1. PRINCIPI FONDAMENTALI (INDEROGABILI)

1.  **Lingua:**
    *   **Commenti, Docstring, Documentazione:** RIGOROSAMENTE IN **ITALIANO**.
    *   **Nomi (Variabili, Funzioni, Classi):** RIGOROSAMENTE IN **INGLESE**.
    *   *Obiettivo:* Codice internazionale, spiegazione locale.

2.  **Chiarezza > Brevità:**
    *   Vietati i "one-liners" complessi.
    *   Vietato l'uso di operatori ternari annidati.
    *   Il codice deve essere leggibile come un libro, dall'alto verso il basso.

3.  **No Magic:**
    *   Nessun side-effect nascosto.
    *   Nessuna dipendenza implicita.
    *   Il flusso dei dati deve essere evidente.

4.  **Fail Fast:**
    *   Validazione degli input **all'inizio** di ogni funzione.
    *   Interrompere l'esecuzione immediatamente se i dati non sono validi.

5.  **RETURN STRICT (Regola Aurea):**
    *   **VIETATO:** `return calculate(a) + b;`
    *   **VIETATO:** `return doSomething();`
    *   **VIETATO (JS Objects):** `return { key: value };`
    *   **OBBLIGATORIO:** Assegnare il risultato a una variabile esplicita prima di ritornarlo.
    *   *Esempio Corretto:*
        ```javascript
        const result = calculate(a) + b;
        return result;
        ```
        *Esempio Factory:*
        ```javascript
        const api = {
            doAction: doAction
        };
        return api;
        ```

---

## 2. JAVASCRIPT (VANILLA CLIENT-SIDE)

**Stack:** Vanilla JS ES6+. Niente jQuery, React, Vue, ecc. (salvo diversa indicazione esplicita).

### Regole Specifiche
*   **Pattern:** Usare il **Factory/Closure Pattern** (stile `ua*.js`) per incapsulare lo stato privato.
*   **Async/Await:** OBBLIGATORIO. Vietato l'uso di `.then()` / `.catch()` (salvo casi limite documentati).
*   **Variabili:** `const` di default. `let` solo se necessario. `var` VIETATO.
*   **DOM:** Manipolazione diretta (`document.getElementById`, `element.style`).

### Template Modulo (Factory Pattern)

```javascript
"use strict";

/**
 * Gestore per [Nome Funzionalità].
 * Descrizione dello scopo del modulo in italiano.
 * 
 * @param {string} containerId - ID dell'elemento contenitore.
 */
const UaMyModule = function(containerId) {
    // 1. STATO PRIVATO
    const _container = document.getElementById(containerId);
    let _internalState = null;

    // 2. FUNZIONI PRIVATE (Helper)
    
    /**
     * Valida i dati in ingresso.
     */
    const _validate = function(data) {
        if (!data) return false;
        return true;
    };

    // 3. FUNZIONI PUBBLICHE (Async preferred)

    /**
     * Esegue l'operazione principale.
     * @returns {Promise<boolean>} Esito operazione.
     */
    const doActionAsync = async function(param) {
        // A. Fail Fast
        if (!_container) {
            console.error("UaMyModule: Container non trovato.");
            return false;
        }

        let success = false;

        try {
            // B. Logica Lineare (No .then)
            const isValid = _validate(param);
            
            if (isValid) {
                // Esempio fetch
                const resp = await fetch('/api/action');
                const data = await resp.json();
                
                _internalState = data;
                success = true;
            }
        } catch (error) {
            console.error("Errore in doActionAsync:", error);
            success = false;
        }

        // C. Return Strict
        return success;
    };

    // 4. API PUBBLICA
    const api = {
        doActionAsync: doActionAsync
    };
    return api;
};
```

---

## 3. PYTHON

**Stack:** Python 3.x. Standard Library preferita.

### Regole Specifiche
*   **Struttura Entry Point:** È OBBLIGATORIO usare la funzione `do_main(...)` chiamata dal blocco `if __name__ == "__main__":`.
*   **Acquisizione Parametri:** I parametri (da `sys.argv` o `argparse`) vanno letti nel blocco main e passati esplicitamente a `do_main`.
*   **Header:** Ogni file deve avere `__date__`, `__version__`, `__author__` e docstring modulo.
*   **Logging:** Usare wrapper o logging standard (es. `teimedlib.ualog`).
*   **Path:** Usare `pathlib` invece di `os.path`.

### Template Script/Modulo

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nome Modulo - Descrizione breve.

Spiegazione dettagliata dello scopo del modulo in italiano.
"""

__date__ = "2026-01-19"
__version__ = "1.0.0"
__author__ = "Gemini CLI"

import sys
import argparse
from pathlib import Path
# import teimedlib.ualog as Log  <-- Se disponibile

def process_file(file_path: str) -> bool:
    """
    Processa un singolo file.
    Helper interno.
    
    Args:
        file_path: Percorso del file.
    Returns:
        bool: Esito.
    """
    # 1. Fail Fast
    if not file_path:
        return False
        
    path_obj = Path(file_path)
    if not path_obj.exists():
        print(f"Errore: File {file_path} non trovato.")
        return False

    result = False

    try:
        # 2. Logica
        content = path_obj.read_text(encoding='utf-8')
        # ... operazioni ...
        result = True
    except Exception as e:
        print(f"Eccezione: {e}")
        result = False

    # 3. Return Strict
    return result

def do_main(input_file: str, verbose: bool = False) -> bool:
    """
    Funzione principale che orchestra la logica (CORE LOGIC).
    
    Args:
        input_file: Path del file input.
        verbose: Flag per output verboso.
    Returns:
        bool: Successo dell'esecuzione.
    """
    if verbose:
        print(f"Avvio elaborazione di: {input_file}")

    # Chiamata a funzioni helper
    success = process_file(input_file)
    
    return success

if __name__ == "__main__":
    # 1. ACQUISIZIONE PARAMETRI
    parser = argparse.ArgumentParser(description="Descrizione dello script")
    parser.add_argument("input_file", help="Path del file da processare")
    parser.add_argument("--verbose", action="store_true", help="Abilita output dettagliato")
    
    args = parser.parse_args()
    
    # 2. CHIAMATA A DO_MAIN
    success = do_main(args.input_file, args.verbose)
    
    # 3. GESTIONE EXIT CODE
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
```

---

## 4. CHECKLIST DI AUTO-REVISIONE (MANDATORIA)

Prima di confermare la generazione del codice, verifico mentalmente:

1.  [ ] **Return Var:** Ho assegnato il valore di ritorno a una variabile prima del `return`? (NO `return fn()`)
2.  [ ] **Lingua:** I commenti sono tutti in Italiano? I nomi del codice in Inglese?
3.  [ ] **Python Main:** Ho usato `do_main` e passato i parametri dal blocco `if __name__ == "__main__":`?
4.  [ ] **Async JS:** Ho usato `await` ed eliminato ogni `.then()`?
5.  [ ] **Fail Fast:** Ho controllato gli input all'inizio della funzione?

