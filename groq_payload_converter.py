
from typing import Any, Dict

# Lista dei parametri ufficialmente supportati dal metodo chat.completions.create di Groq.
# Fonte: Documentazione API di Groq e compatibilità con OpenAI.
SUPPORTED_GROQ_PARAMS = {
    "messages",
    "model",
    "frequency_penalty",
    "logit_bias",
    "logprobs",
    "max_tokens",
    "n",
    "presence_penalty",
    "response_format",
    "seed",
    "stop",
    "stream",
    "temperature",
    "top_p",
    "top_logprobs",
    "tool_choice",
    "tools",
    "user",
}

def convert_to_groq_payload(openai_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filtra e valida un payload in stile OpenAI per renderlo compatibile
    con l'API Groq.

    Poiché l'API di Groq è già conforme a quella di OpenAI, questa funzione
    serve principalmente a garantire che solo i parametri supportati vengano
    inoltrati, rimuovendo eventuali campi non validi e valori None.

    Args:
        openai_payload: Un dizionario contenente i parametri della richiesta
                        in stile OpenAI.

    Returns:
        Un dizionario di argomenti pulito e pronto per essere passato
        al client Groq.
    """
    groq_payload = {
        key: value
        for key, value in openai_payload.items()
        if key in SUPPORTED_GROQ_PARAMS and value is not None
    }
    return groq_payload
