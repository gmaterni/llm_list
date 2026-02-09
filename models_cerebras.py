#!/usr/bin/env python3
"""
Script per ottenere i modelli Cerebras e salvarli in file.
"""

import os
import requests
from pathlib import Path

def filter_and_sort_models(models):
    """
    HIGHLIGHT: Filtri di selezione
    1. Per Cerebras, includiamo tutti i modelli restituiti dall'API.
    2. Raggruppa per nome base e mantiene il più recente se applicabile.
    """
    latest_models = {}
    for m in models:
        model_id = m.get("id")
        parts = model_id.split("-")
        if len(parts) > 1 and parts[-1].isdigit():
            base_name = "-".join(parts[:-1])
            version = parts[-1]
        else:
            base_name = model_id
            version = "000"
            
        if base_name not in latest_models:
            latest_models[base_name] = (version, m)
        else:
            current_version, _ = latest_models[base_name]
            if version > current_version:
                latest_models[base_name] = (version, m)
                
    return [item[1] for item in latest_models.values()]

def main():
    api_key = os.getenv("CEREBRAS_API_KEY")
    if not api_key:
        print("ERRORE: Imposta la variabile d'ambiente CEREBRAS_API_KEY")
        return
    
    url = "https://api.cerebras.ai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        all_models = response.json().get("data", [])
        
        filtered_models = filter_and_sort_models(all_models)
        
        Path("data").mkdir(exist_ok=True)
        
        def get_context_window(model_id):
            if "llama-3.1" in model_id or "llama-3.3" in model_id:
                return 131072 # 128k
            if "llama3" in model_id:
                return 8192
            return 8192 # Default
        
        # 1. Salva lista nomi
        with open("data/models_cerebras.txt", "w") as f:
            for m in sorted(filtered_models, key=lambda x: x.get("id")):
                f.write(f"{m.get('id')}\n")
        
        # 2. Salva nomi e finestra (wnd)
        with open("data/models_cerebras_wnd.txt", "w") as f:
            for m in sorted(filtered_models, key=lambda x: x.get("id")):
                model_id = m.get("id")
                limit = get_context_window(model_id)
                k_limit = f"{limit // 1024}k" if limit >= 1024 else f"{limit}"
                f.write(f"{model_id}|{k_limit}\n")
                
        # 3. Salva info dettagliate
        with open("data/models_cerebras_info.txt", "w") as f:
            f.write("MODELLI CEREBRAS - INFORMAZIONI DETTAGLIATE\n")
            f.write("=" * 50 + "\n\n")
            for m in sorted(filtered_models, key=lambda x: x.get("id")):
                model_id = m.get("id")
                f.write(f"ID: {model_id}\n")
                f.write(f"Created: {m.get('created')}\n")
                f.write(f"Owned By: {m.get('owned_by')}\n")
                f.write(f"Context (est.): {get_context_window(model_id)}\n")
                f.write("-" * 30 + "\n")

        print(f"Completato! Salvati {len(filtered_models)} modelli Cerebras in data/")
        
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()