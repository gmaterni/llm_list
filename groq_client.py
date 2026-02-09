
import os
from typing import Any, Dict, List

from groq import Groq

from .base_client import ErrorLLM, LLMClient, ResponseLLM
from .groq_payload_converter import convert_to_groq_payload

class GroqClient(LLMClient):
    """
    Client per interagire con l'API di Groq.
    
    Questa classe implementa l'interfaccia LLMClient per fornire una
    comunicazione standardizzata con i modelli Groq.
    """
    def __init__(self, 
                 api_key: str = "", 
                 api_key_env_var: str = "GROQ_API_KEY"):
        """
        Inizializza il client Groq.
        
        Args:
            api_key (str, optional): La chiave API di Groq. Se non fornita,
                                     verrà cercata nella variabile d'ambiente
                                     specificata da `api_key_env_var`.
            api_key_env_var (str, optional): Nome della variabile d'ambiente per
                                             la chiave API. Default: "GROQ_API_KEY".
        """
        super().__init__(api_key, api_key_env_var)
        self.client = Groq(api_key=self.api_key)

    def send_request(self, payload: Dict[str, Any]) -> ResponseLLM:
        """
        Invia una richiesta a Groq e restituisce la risposta.
        
        Args:
            payload (Dict[str, Any]): Payload in stile OpenAI.
        
        Returns:
            ResponseLLM: Oggetto contenente i dati o l'errore.
        """
        try:
            groq_payload = convert_to_groq_payload(payload)
            response = self.client.chat.completions.create(**groq_payload)
            response_content = response.choices[0].message.content
            
            usage = None
            if hasattr(response, 'usage'):
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }

            return ResponseLLM(data=response_content, usage=usage)

        except Exception as e:
            error = ErrorLLM(
                message=str(e),
                type=e.__class__.__name__,
                code=getattr(e, 'code', None),
                details=str(e)
            )
            return ResponseLLM(error=error)

    def embed(self, model_name: str, texts: List[str]) -> List[List[float]]:
        """
        Metodo non implementato per Groq, poiché l'API principale non supporta l'embedding.
        """
        raise NotImplementedError("Groq API does not support embedding.")

# Esempio di utilizzo (da eseguire come script a sé stante)
if __name__ == '__main__':
    
    try:
        client = GroqClient()
        
        # Esempio di payload stile OpenAI
        example_payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": "Ciao, come ti chiami?"}
            ],
            "temperature": 0.7,
            "max_tokens": 150,
            "stream": False
        }
        
        response = client.send_request(example_payload)
        
        if response.error:
            print(f"Errore durante la richiesta: {response.error}")
        else:
            print("Risposta dal modello:")
            print(response.data)
            
    except ValueError as e:
        print(e)
    except ImportError:
        print("Per eseguire questo esempio, installa la libreria: pip install groq")
