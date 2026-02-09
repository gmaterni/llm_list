#!/usr/bin/env python3
"""
Script per ottenere i modelli Gemini filtrati e salvarli in file.
"""

import os
from google import genai
from pathlib import Path

def filter_and_sort_models(models):
    """
    HIGHLIGHT: Filtri di selezione
    1. Solo modelli che supportano la generazione di testo (generateContent).
    2. Per modelli con lo stesso nome base, mantiene solo il più aggiornato.
    """
    text_models = [m for m in models if "generateContent" in m.supported_actions]
    
    latest_models = {}
    for m in text_models:
        name = m.name.replace("models/", "")
        parts = name.split('-')
        
        if parts[-1].isdigit():
            base_name = "-".join(parts[:-1])
            version = parts[-1]
        else:
            base_name = name
            version = "000"
            
        if base_name not in latest_models:
            latest_models[base_name] = (version, m)
        else:
            current_version, _ = latest_models[base_name]
            if version > current_version:
                latest_models[base_name] = (version, m)
                 
    return [item[1] for item in latest_models.values()]

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERRORE: Imposta la variabile d'ambiente GEMINI_API_KEY")
        return
    
    client = genai.Client(api_key=api_key)
    all_models = list(client.models.list())
    
    filtered_models = filter_and_sort_models(all_models)
    
    Path("data").mkdir(exist_ok=True)
    
    # 1. Salva lista nomi
    with open("data/models_gemini.txt", "w") as f:
        for m in sorted(filtered_models, key=lambda x: x.name):
            clean_name = m.name.replace("models/", "")
            f.write(f"{clean_name}\n")
            
    # 2. Salva nomi e finestra di input (wnd)
    with open("data/models_gemini_wnd.txt", "w") as f:
        for m in sorted(filtered_models, key=lambda x: x.name):
            clean_name = m.name.replace("models/", "")
            limit = getattr(m, 'input_token_limit', 0)
            k_limit = f"{limit // 1024}k" if limit >= 1024 else f"{limit}"
            f.write(f"{clean_name}|{k_limit}\n")

    # 3. Salva info dettagliate
    with open("data/models_gemini_info.txt", "w") as f:
        f.write("MODELLI GEMINI - INFORMAZIONI DETTAGLIATE\n")
        f.write("=" * 50 + "\n\n")
        for m in sorted(filtered_models, key=lambda x: x.name):
            clean_name = m.name.replace("models/", "")
            f.write(f"ID: {clean_name}\n")
            f.write(f"Display Name: {m.display_name}\n")
            if hasattr(m, 'version'): f.write(f"Version: {m.version}\n")
            if hasattr(m, 'input_token_limit'): f.write(f"Input Limit: {m.input_token_limit}\n")
            if hasattr(m, 'output_token_limit'): f.write(f"Output Limit: {m.output_token_limit}\n")
            f.write("-" * 30 + "\n")

    print(f"Completato! Salvati {len(filtered_models)} modelli Gemini in data/")

if __name__ == "__main__":
    main()