#!/usr/bin/env python3
"""
Script per ottenere i modelli Groq e salvarli in file.
"""

import os
from pathlib import Path
from groq import Groq


def filter_and_sort_models(models):
    """
    HIGHLIGHT: Filtri di selezione
    1. Solo modelli che supportano la generazione di testo.
    2. Per modelli con lo stesso nome, mantiene il più aggiornato.
    """
    # In Groq, tutti i modelli supportano la generazione di testo
    # quindi li includiamo tutti
    filtered = models

    latest_models = {}
    for m in filtered:
        model_id = m.id
        name_parts = model_id.split("/")
        provider = name_parts[0] if len(name_parts) > 0 else ""
        model_name = name_parts[1] if len(name_parts) > 1 else model_id

        parts = model_name.split(":")
        base_name = f"{provider}/{parts[0]}" if provider else parts[0]
        version = parts[1] if len(parts) > 1 else "000"

        if base_name not in latest_models:
            latest_models[base_name] = (version, m)
        else:
            current_version, _ = latest_models[base_name]
            if version > current_version:
                latest_models[base_name] = (version, m)

    return [item[1] for item in latest_models.values()]


def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERRORE: Imposta la variabile d'ambiente GROQ_API_KEY")
        return

    try:
        client = Groq(api_key=api_key)
        
        # Otteniamo i modelli disponibili da Groq
        # A differenza di OpenRouter, Groq non ha un endpoint dedicato per elencare i modelli
        # Quindi useremo una lista predefinita dei modelli Groq attualmente disponibili
        # In alternativa, potremmo tentare di ottenere informazioni sui modelli disponibili
        
        # Lista dei modelli Groq attualmente disponibili (aggiornata manualmente)
        available_models = [
            {"id": "llama3-8b-8192", "name": "Llama 3 8B", "context_length": 8192},
            {"id": "llama3-70b-8192", "name": "Llama 3 70B", "context_length": 8192},
            {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B", "context_length": 32768},
            {"id": "gemma-7b-it", "name": "Gemma 7B", "context_length": 8192},
            {"id": "gemma2-9b-it", "name": "Gemma 2 9B", "context_length": 8192},
            {"id": "llama-3.1-8b-instant", "name": "Llama 3.1 8B (Instant)", "context_length": 131072},
            {"id": "llama-3.1-70b-versatile", "name": "Llama 3.1 70B (Versatile)", "context_length": 131072},
            {"id": "llama-3.2-1b-preview", "name": "Llama 3.2 1B (Preview)", "context_length": 8192},
            {"id": "llama-3.2-3b-preview", "name": "Llama 3.2 3B (Preview)", "context_length": 8192},
            {"id": "llama-guard-3-8b", "name": "Llama Guard 3 8B", "context_length": 8192},
        ]

        # Convertiamo i dizionari in oggetti simili a quelli usati dagli altri script
        class ModelObject:
            def __init__(self, model_dict):
                for key, value in model_dict.items():
                    setattr(self, key, value)

        model_objects = [ModelObject(model) for model in available_models]
        filtered_models = filter_and_sort_models(model_objects)

        Path("data").mkdir(exist_ok=True)

        # 1. Salva lista nomi
        with open("data/models_groq.txt", "w") as f:
            for m in sorted(filtered_models, key=lambda x: x.id):
                f.write(f"{m.id}\n")

        # 2. Salva nomi e finestra (wnd)
        with open("data/models_groq_wnd.txt", "w") as f:
            for m in sorted(filtered_models, key=lambda x: x.id):
                limit = m.context_length
                k_limit = f"{limit // 1024}k" if limit >= 1024 else f"{limit}"
                f.write(f"{m.id}|{k_limit}\n")

        # 3. Salva info dettagliate
        with open("data/models_groq_info.txt", "w") as f:
            f.write("MODELLI GROQ - INFORMAZIONI DETTAGLIATE\n")
            f.write("=" * 50 + "\n\n")
            for m in sorted(filtered_models, key=lambda x: x.id):
                f.write(f"ID: {m.id}\n")
                f.write(f"Nome: {m.name}\n")
                f.write(f"Context: {m.context_length}\n")
                f.write("-" * 30 + "\n")

        print(f"Completato! Salvati {len(filtered_models)} modelli Groq in data/")

    except Exception as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    main()