#!/usr/bin/env python3
"""
Script models_test.py per testare i modelli di vari provider.
Legge i modelli da data/<provider>.txt e salva quelli funzionanti in data/<provider>_ok.txt.
"""

import os
import requests
import time
import sys
from pathlib import Path


def get_wnd_map(provider):
    """Legge il file _wnd.txt per ottenere la mappatura id|wnd."""
    wnd_map = {}
    wnd_file = Path("data") / f"models_{provider}_wnd.txt"
    if wnd_file.exists():
        with open(wnd_file, "r") as f:
            for line in f:
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) >= 2:
                        model_id, wnd = parts[0], parts[1]
                        wnd_map[model_id] = wnd
    return wnd_map


def test_gemini(model_id, api_key):
    # Prova diverse varianti di URL per Gemini
    base_url = "https://generativelanguage.googleapis.com/v1beta"

    # Assicurati che l'ID sia nel formato corretto per l'URL
    if not model_id.startswith("models/"):
        model_id_for_url = f"models/{model_id}"
    else:
        model_id_for_url = model_id

    url = f"{base_url}/{model_id_for_url}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        # Fallback a v1
        url_v1 = url.replace("/v1beta/", "/v1/")
        response = requests.post(url_v1, json=payload, timeout=10)
        return response.status_code == 200
    except:
        return False


def test_openai_compatible(url, model_id, api_key):
    headers = {"Authorization": f"Bearer {api_key}",
               "Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 5
    }
    try:
        response = requests.post(url, headers=headers,
                                 json=payload, timeout=10)
        return response.status_code == 200
    except:
        return False


def main():
    data_path = Path("data")
    if not data_path.exists():
        print("Cartella data non trovata.")
        return

    # Usiamo glob ma filtriamo manualmente per evitare problemi con file ignorati se possibile
    # In questo ambiente, l'agente può vedere i file via shell meglio che via glob python su alcune config
    all_providers = ["gemini", "groq", "mistral",
                     "cerebras", "openrouter", "huggingface"]

    target_provider = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if target_provider:
        if target_provider not in all_providers:
            print(
                f"Provider '{target_provider}' non riconosciuto. Disponibili: {', '.join(all_providers)}")
            return
        providers = [target_provider]
    else:
        providers = all_providers

    endpoints = {
        "groq": "https://api.groq.com/openai/v1/chat/completions",
        "mistral": "https://api.mistral.ai/v1/chat/completions",
        "cerebras": "https://api.cerebras.ai/v1/chat/completions",
        "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    }

    for provider in sorted(providers):
        model_file = data_path / f"models_{provider}.txt"
        if not model_file.exists():
            continue

        print(f"Testing provider: {provider}")

        env_var = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_var)
        if provider == "openrouter" and not api_key:
            api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv(
                "OPENAI_API_KEY")
        if provider == "huggingface" and not api_key:
            api_key = os.getenv("HF_TOKEN")

        if not api_key:
            print(f"  Skipping {provider}: API key ({env_var}) not found.")
            continue

        try:
            with open(model_file, "r") as f:
                models = [line.strip() for line in f if line.strip()]
        except:
            print(f"  Errore nella lettura di {model_file}")
            continue

        wnd_map = get_wnd_map(provider)
        ok_models = []

        for model_id in models:
            print(f" Testing {model_id}... ", end="", flush=True)
            success = False

            if provider == "gemini":
                success = test_gemini(model_id, api_key)
            elif provider in endpoints:
                success = test_openai_compatible(
                    endpoints[provider], model_id, api_key)
            elif provider == "huggingface":
                url = f"https://api-inference.huggingface.co/models/{model_id}"
                headers = {"Authorization": f"Bearer {api_key}"}
                try:
                    res = requests.post(url, headers=headers, json={
                                        "inputs": "hi"}, timeout=10)
                    success = (res.status_code == 200)
                except:
                    success = False
            else:
                success = False

            if success:
                print("OK")
                wnd = wnd_map.get(model_id, "N/A")
                ok_models.append(f"{model_id}|{wnd}")
            else:
                print("FAILED")

            # Delay di 5 secondi tra richieste dello stesso provider
            time.sleep(5.0)

        if ok_models:
            output_dir = Path("data_ok")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{provider}_wnd.txt"
            with open(output_file, "w") as f:
                for line in ok_models:
                    f.write(f"{line}\n")
            print(
                f"  Completato! Salvati {len(ok_models)} modelli in {output_file}")
        else:
            print(f"  Nessun modello funzionante trovato per {provider}.")


if __name__ == "__main__":
    main()
