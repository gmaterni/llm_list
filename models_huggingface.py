#!/usr/bin/env python3
"""
Script per ottenere i modelli HuggingFace filtrati e salvarli in file.
"""

import os
import requests
from pathlib import Path

def filter_and_sort_models(models):
    """
    HIGHLIGHT: Filtri di selezione
    1. Solo modelli di tipo 'text-generation'.
    2. Su HF, consideriamo "free" i modelli pubblici e più popolari 
       che solitamente sono disponibili via Inference API gratuita.
    3. Per modelli con lo stesso nome base, mantiene il più scaricato/aggiornato.
    """
    filtered = [m for m in models if m.get("pipeline_tag") == "text-generation"]
    
    latest_models = {}
    for m in filtered:
        model_id = m.get("modelId", m.get("id"))
        base_name = model_id.split("/")[-1]
        
        if base_name not in latest_models:
            latest_models[base_name] = m
        else:
            if m.get("downloads", 0) > latest_models[base_name].get("downloads", 0):
                latest_models[base_name] = m
                
    return list(latest_models.values())

def main():
    token = os.getenv("HF_TOKEN")
    
    url = "https://huggingface.co/api/models"
    params = {
        "filter": "text-generation",
        "sort": "downloads",
        "direction": -1,
        "limit": 100
    }
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        all_models = response.json()
        
        filtered_models = filter_and_sort_models(all_models)
        
        Path("data").mkdir(exist_ok=True)
        
        # 1. Salva lista nomi
        with open("data/models_huggingface.txt", "w") as f:
            for m in sorted(filtered_models, key=lambda x: x.get("id")):
                model_id = m.get("id")
                f.write(f"{model_id}\n")
        
        # 2. Salva nomi e finestra (wnd)
        # Nota: HF API non fornisce sempre window_size direttamente nel list
        with open("data/models_huggingface_wnd.txt", "w") as f:
            for m in sorted(filtered_models, key=lambda x: x.get("id")):
                model_id = m.get("id")
                f.write(f"{model_id}|N/A\n")
                
        # 3. Salva info dettagliate
        with open("data/models_huggingface_info.txt", "w") as f:
            f.write("MODELLI HUGGINGFACE - INFORMAZIONI DETTAGLIATE\n")
            f.write("=" * 50 + "\n\n")
            for m in sorted(filtered_models, key=lambda x: x.get("id")):
                f.write(f"ID: {m.get('id')}\n")
                f.write(f"Pipeline: {m.get('pipeline_tag')}\n")
                f.write(f"Downloads: {m.get('downloads')}\n")
                f.write(f"Likes: {m.get('likes')}\n")
                f.write("-" * 30 + "\n")

        print(f"Completato! Salvati {len(filtered_models)} modelli HuggingFace in data/")
        
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()
