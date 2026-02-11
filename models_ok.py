#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Selezione Modelli Ottimali - Filtra, testa e ordina i modelli LLM.

Questo script seleziona i modelli migliori da vari provider, filtrandoli in base alla loro idoneità alla chat e alla risposta a query semantiche.
Successivamente, li ordina per velocità di risposta e dimensione della finestra di input per identificare i più performanti.
"""

__date__ = "2026-02-11"
__version__ = "1.1.0"
__author__ = "Gemini CLI"

import os
import sys
import argparse
import requests
import time
from pathlib import Path


def get_model_specs(provider: str) -> list:
    """Legge le specifiche dei modelli dai file data."""
    data_path = Path("data")

    # Leggi la lista dei modelli
    model_file = data_path / f"models_{provider}.txt"
    if not model_file.exists():
        print(f"File {model_file} non trovato")
        return []

    with open(model_file, "r") as f:
        models = [line.strip() for line in f if line.strip()]

    # Leggi le dimensioni delle finestre
    wnd_file = data_path / f"models_{provider}_wnd.txt"
    wnd_map = {}
    if wnd_file.exists():
        with open(wnd_file, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 2:
                    model_id, wnd = parts[0], parts[1]
                    wnd_map[model_id] = wnd

    # Costruisci le specifiche
    model_specs = []
    for model_id in models:
        window = wnd_map.get(model_id, "N/A")

        try:
            if isinstance(window, str) and window.lower().endswith('k'):
                window_val = int(window[:-1]) * 1024
            else:
                window_val = int(window)
        except (ValueError, TypeError):
            window_val = 0

        model_specs.append((model_id, window_val, 0))

    return model_specs


def get_chat_capable_models() -> dict:
    """Identifica i modelli capaci di gestire conversazioni chat."""
    chat_models = {}
    data_path = Path("data")

    info_files = list(data_path.glob("*_info.txt"))

    for info_file in info_files:
        provider = info_file.name.replace(
            "models_", "").replace("_info.txt", "")
        current_models = []
        content = info_file.read_text(encoding='utf-8')

        model_entries = content.split("------------------------------")
        for entry in model_entries:
            entry = entry.strip()
            if not entry:
                continue

            model_id = None
            if "ID:" in entry:
                model_id_line = next((line for line in entry.split(
                    '\n') if line.strip().startswith("ID:")), None)
                if model_id_line:
                    model_id = model_id_line.split("ID:", 1)[1].strip()

            if not model_id:
                continue

            if provider == "huggingface":
                if "Pipeline: text-generation" in entry:
                    current_models.append(model_id)
            elif provider == "openrouter":
                if "Modality: text->text" in entry or "Modality: text+image->text" in entry:
                    current_models.append(model_id)
            else:
                if provider in ["cerebras", "groq"]:
                    current_models.append(model_id)
                elif provider == "gemini":
                    if not any(keyword in model_id.lower() for keyword in ["image", "tts", "robotics"]):
                        current_models.append(model_id)
                elif provider == "mistral":
                    if not any(keyword in model_id.lower() for keyword in ["pixtral", "voxtral"]):
                        current_models.append(model_id)

        if current_models:
            chat_models[provider] = current_models

    return chat_models


def test_model_performance(provider: str, model_id: str, api_key: str, query: str) -> tuple:
    """Testa le prestazioni di un modello e restituisce esito, tempo, validità, lunghezza e errore."""
    endpoints = {
        "groq": "https://api.groq.com/openai/v1/chat/completions",
        "mistral": "https://api.mistral.ai/v1/chat/completions",
        "cerebras": "https://api.cerebras.ai/v1/chat/completions",
        "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    }

    success = False
    response_time = 999.0
    valid_response = False
    response_length = 0
    error_msg = ""

    start_time = time.time()

    try:
        if provider == "gemini":
            base_url = "https://generativelanguage.googleapis.com/v1beta"
            model_url = f"models/{model_id}" if not model_id.startswith(
                "models/") else model_id
            url = f"{base_url}/{model_url}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": query}]}]}
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if "candidates" in data and data["candidates"]:
                    text = data["candidates"][0].get("content", {}).get(
                        "parts", [{}])[0].get("text", "")
                    if text.strip():
                        valid_response = True
                        success = True
                        response_length = len(text)
                else:
                    error_msg = "Nessun contenuto generato"
            else:
                error_msg = f"HTTP {resp.status_code}"

        elif provider in endpoints:
            url = endpoints[provider]
            headers = {"Authorization": f"Bearer {api_key}",
                       "Content-Type": "application/json"}
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": query}],
                "max_tokens": 500
            }
            resp = requests.post(url, headers=headers,
                                 json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if "choices" in data and data["choices"]:
                    text = data["choices"][0].get(
                        "message", {}).get("content", "")
                    if text.strip():
                        valid_response = True
                        success = True
                        response_length = len(text)
                else:
                    error_msg = "Nessuna scelta restituita"
            else:
                try:
                    err_json = resp.json()
                    error_msg = err_json.get("error", {}).get(
                        "message", f"HTTP {resp.status_code}")
                except:
                    error_msg = f"HTTP {resp.status_code}"

        elif provider == "huggingface":
            url = f"https://api-inference.huggingface.co/models/{model_id}"
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {"inputs": query}
            resp = requests.post(url, headers=headers,
                                 json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                text = ""
                if isinstance(data, list) and data:
                    text = data[0].get("generated_text", "")
                elif isinstance(data, dict):
                    text = data.get("generated_text", "")

                if text.strip():
                    valid_response = True
                    success = True
                    response_length = len(text)
                else:
                    error_msg = "Testo vuoto"
            else:
                error_msg = f"HTTP {resp.status_code}"

    except requests.exceptions.Timeout:
        error_msg = "Timeout"
    except Exception as e:
        error_msg = str(e)[:50]

    end_time = time.time()
    if success:
        response_time = end_time - start_time

    result = (success, response_time, valid_response,
              response_length, error_msg)
    return result


def filter_and_sort_models(models_tested: list) -> list:
    """Filtra i modelli con successo e li ordina per tempo di risposta."""
    successful_models = [m for m in models_tested if m[3]]
    sorted_models = sorted(successful_models, key=lambda x: x[4])
    return sorted_models


def do_main(input_provider: str) -> bool:
    """Orchestra la logica per la selezione dei modelli."""
    provider = input_provider.lower()

    env_var = f"{provider.upper()}_API_KEY"
    api_key = os.getenv(env_var)
    if provider == "openrouter" and not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv(
            "OPENAI_API_KEY")
    if provider == "huggingface" and not api_key:
        api_key = os.getenv("HF_TOKEN")

    if not api_key:
        print(f"Errore: Chiave API per {provider} non trovata.")
        return False

    all_chat_models = get_chat_capable_models()
    chat_models_for_provider = all_chat_models.get(provider, [])

    if not chat_models_for_provider:
        print(f"Nessun modello chat-capable trovato per {provider}")
        return False

    all_models_specs = get_model_specs(provider)
    models_to_test = [
        spec for spec in all_models_specs if spec[0] in chat_models_for_provider]

    if not models_to_test:
        print(f"Nessun modello chat-capable trovato in data per {provider}")
        return False

    print(
        f"Avvio test prestazioni per {len(models_to_test)} modelli di {provider}...")
    query_italiana = "Spiegami brevemente l'importanza di Dante Alighieri per la lingua italiana e la cultura europea."

    tested_results = []
    for model_id, window, _ in models_to_test:
        print(f"{model_id:30} ...", end="", flush=True)

        success, resp_time, valid, resp_len, err = test_model_performance(
            provider, model_id, api_key, query_italiana)

        if success and valid:
            print(f"OK ({resp_time:.2f}s, {resp_len} car.)")
            tested_results.append((model_id, window, 0, True, resp_time))
        else:
            # Tronca l'errore se troppo lungo
            err_short = (err[:30] + '..') if len(err) > 30 else err
            print(f"FAILED ({err_short})")
            tested_results.append((model_id, window, 0, False, 999.0))

        time.sleep(2.0)

    best_models = filter_and_sort_models(tested_results)

    if not best_models:
        print(f"\nNessun modello ha superato il test per {provider}.")
        return False

    print(f"\nMigliori modelli per {provider} (ordinati per velocità):")
    for i, (model_id, window, _, _, resp_time) in enumerate(best_models, 1):
        print(f"{i}. {model_id}: tempo={resp_time:.2f}s, finestra={window}")

    output_dir = Path("data_ok")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{provider}_wnd.txt"

    try:
        with open(output_file, "w") as f:
            for model_id, window, _, _, _ in best_models:
                f.write(f"{model_id}|{window}\n")
        print(f"\nSalvati {len(best_models)} modelli in {output_file}")
        return True
    except Exception as e:
        print(f"Errore scrittura output: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seleziona i modelli migliori di un provider.")
    parser.add_argument("provider", help="Nome del provider")
    args = parser.parse_args()
    if do_main(args.provider):
        sys.exit(0)
    else:
        sys.exit(1)
