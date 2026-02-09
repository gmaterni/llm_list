import os
import json
import glob
from llmclient.gemini_client import GeminiClient
from llmclient.groq_client import GroqClient
from llmclient.mistral_client import MistralClient
from llmclient.huggingface_client import HuggingFaceClient
from llmclient.openrouter_client import OpenRouterClient

class LlmProvider:
    def __init__(self):
        self.clients = {}
        self.provider_config = {}
        self.config = {
            "provider": "",
            "model": "",
            "windowSize": 0,
            "client": "",
        }
        self.api_keys = {}
        self._load_api_keys()
        self._load_provider_config()
        self._init_clients()
        
        # Imposta un default se possibile
        if self.provider_config:
            p = next(iter(self.provider_config))
            m = next(iter(self.provider_config[p]["models"]))
            self.set_config(p, m)

    def _load_api_keys(self):
        try:
            if os.path.exists("api_keys.json"):
                with open("api_keys.json", "r") as f:
                    data = json.load(f)
                    for provider, info in data.get("providers", {}).items():
                        exported_key_name = info.get("exported_key")
                        for key_info in info.get("keys", []):
                            if key_info.get("name") == exported_key_name:
                                self.api_keys[provider] = key_info.get("key")
                                break
                        if provider not in self.api_keys and info.get("keys"):
                            self.api_keys[provider] = info["keys"][0]["key"]
        except Exception as e:
            print(f"Errore nel caricamento delle chiavi API: {e}")

    def _load_provider_config(self):
        data_dir = "data"
        if not os.path.exists(data_dir):
            return
        files = glob.glob(os.path.join(data_dir, "models_*_wnd.txt"))
        for file_path in files:
            filename = os.path.basename(file_path)
            provider_name = filename.replace("models_", "").replace("_wnd.txt", "")
            
            models = {}
            try:
                with open(file_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and "|" in line:
                            parts = line.split("|")
                            if len(parts) >= 2:
                                model_name, window_size_str = parts[0], parts[1]
                                # Convert 1024k to integer 1024
                                size_val = window_size_str.lower().replace("k", "")
                                try:
                                    size_val = int(size_val)
                                except:
                                    size_val = 0
                                models[model_name] = {"windowSize": size_val}
                
                if models:
                    self.provider_config[provider_name] = {
                        "client": provider_name,
                        "models": models
                    }
            except Exception as e:
                print(f"Errore nel caricamento del file {file_path}: {e}")

    def _init_clients(self):
        # OpenRouter might use 'openai' key if available in api_keys.json
        or_key = self.api_keys.get("openrouter") or self.api_keys.get("openai")
        
        mapping = {
            "gemini": GeminiClient,
            "groq": GroqClient,
            "mistral": MistralClient,
            "huggingface": HuggingFaceClient,
            "openrouter": OpenRouterClient
        }
        
        for name, client_class in mapping.items():
            key = self.api_keys.get(name)
            if name == "openrouter" and not key:
                key = or_key
            
            if key:
                self.clients[name] = client_class(key)

    def set_config(self, provider, model):
        if provider in self.provider_config and model in self.provider_config[provider]["models"]:
            self.config = {
                "provider": provider,
                "model": model,
                "windowSize": self.provider_config[provider]["models"][model]["windowSize"],
                "client": self.provider_config[provider].get("client", provider)
            }
            return True
        return False

    def get_client(self, client_name=None):
        if client_name is None:
            client_name = self.config.get("client")
        return self.clients.get(client_name)

    def get_config(self):
        return self.config

    def get_provider_config(self):
        return self.provider_config

    def reload(self):
        """Ricarica le chiavi API e la configurazione dei modelli dai file."""
        self.provider_config = {}
        self.api_keys = {}
        self._load_api_keys()
        self._load_provider_config()
        self._init_clients()
        return True

# Singleton instance
llm_provider = LlmProvider()
