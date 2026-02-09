#!/usr/bin/env python3
"""
Script per ottenere i modelli Mistral filtrati e salvarli in file.
"""

import os
from mistralai import Mistral
from pathlib import Path

def filter_and_sort_models(models_data):
    """
    HIGHLIGHT: Filtri di selezione
    1. Solo modelli che supportano la chat (completion_chat).
    2. Raggruppa per nome base e mantiene il più recente.
    """
    filtered = []
    for model in models_data:
        capabilities = getattr(model, 'capabilities', None)
        if capabilities and getattr(capabilities, 'completion_chat', False):
            filtered.append(model)
            
    latest_models = {}
    for m in filtered:
        base_id = m.id
        parts = base_id.split('-')
        
        if len(parts) > 1 and parts[-1].isdigit():
            base_name = "-".join(parts[:-1])
            version = parts[-1]
        else:
            base_name = base_id
            version = "000"
            
        if "latest" in base_id:
            version = "999"
            
        if base_name not in latest_models:
            latest_models[base_name] = (version, m)
        else:
            current_version, _ = latest_models[base_name]
            if version > current_version:
                latest_models[base_name] = (version, m)
                
    return [item[1] for item in latest_models.values()]

def main():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("ERRORE: Imposta la variabile d'ambiente MISTRAL_API_KEY")
        return
    
    client = Mistral(api_key=api_key)
    response = client.models.list()
    
    filtered_models = filter_and_sort_models(response.data)
    
    Path("data").mkdir(exist_ok=True)
    
    # 1. Salva lista nomi
    with open("data/models_mistral.txt", "w") as f:
        for m in sorted(filtered_models, key=lambda x: x.id):
            f.write(f"{m.id}\n")
            
    # 2. Salva nomi e finestra (wnd)
    with open("data/models_mistral_wnd.txt", "w") as f:
        for m in sorted(filtered_models, key=lambda x: x.id):
            limit = getattr(m, 'max_context_length', 0)
            k_limit = f"{limit // 1024}k" if limit >= 1024 else f"{limit}"
            f.write(f"{m.id}|{k_limit}\n")

    # 3. Salva info dettagliate
    with open("data/models_mistral_info.txt", "w") as f:
        f.write("MODELLI MISTRAL - INFORMAZIONI DETTAGLIATE\n")
        f.write("=" * 50 + "\n\n")
        for m in sorted(filtered_models, key=lambda x: x.id):
            f.write(f"ID: {m.id}\n")
            if hasattr(m, 'name'): f.write(f"Nome: {m.name}\n")
            if hasattr(m, 'max_context_length'): f.write(f"Context: {m.max_context_length}\n")
            f.write("-" * 30 + "\n")

    print(f"Completato! Salvati {len(filtered_models)} modelli Mistral in data/")

if __name__ == "__main__":
    main()