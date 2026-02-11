# Modelli Gratuiti OpenRouter - Guida Completa

Questo documento elenca i migliori modelli AI gratuiti disponibili su OpenRouter, ordinati per velocità e caratteristiche. Per ogni modello è riportato il nome API esatto da utilizzare nelle chiamate.

⚠️ **IMPORTANTE**: Per utilizzare i modelli gratuiti devi attivare l'opzione 'Model Training' nelle impostazioni privacy di OpenRouter.

---

## 🚀 MODELLI VELOCI E COMPATTI

### Google Gemma 3 (27B)
**Nome API**: `google/gemma-3-27b-it:free`
- **Velocità**: Molto Alta
- **Context**: 128K token
- **Multilingua**: Eccellente
- **Note**: Ottimo per chat rapide e dialoghi quotidiani

### Google Gemma 3 (12B)
**Nome API**: `google/gemma-3-12b-it:free`
- **Velocità**: Molto Alta
- **Context**: 128K token
- **Multilingua**: Eccellente
- **Note**: Versione più veloce, ideale per risposte immediate

### Meta Llama 3.3 (70B)
**Nome API**: `meta-llama/llama-3.3-70b-instruct:free`
- **Velocità**: Alta
- **Context**: 128K token
- **Multilingua**: Ottimo (IT, FR, DE, ES, PT)
- **Note**: Eccellente per conversazioni multilingua complesse

### Meta Llama 4 Scout
**Nome API**: `meta-llama/llama-4-scout:free`
- **Velocità**: Alta
- **Context**: 256K token
- **Multilingua**: Ottimo
- **Note**: Modello multimodale (testo + immagini)

### Meta Llama 4 Maverick
**Nome API**: `meta-llama/llama-4-maverick:free`
- **Velocità**: Alta
- **Context**: 1M token
- **Multilingua**: Ottimo
- **Note**: Context window enorme per documenti lunghi

---

## 💪 MODELLI POTENTI (Output Dettagliato)

### DeepSeek Chat V3
**Nome API**: `deepseek/deepseek-chat-v3-0324:free`
- **Velocità**: Media
- **Context**: 64K token
- **Multilingua**: Buono
- **Note**: Molto dettagliato, ottimo per coding. ⚠️ Server in Cina

### DeepSeek R1
**Nome API**: `deepseek/deepseek-r1:free`
- **Velocità**: Lenta
- **Context**: 64K token
- **Multilingua**: Buono
- **Note**: Con ragionamento esplicito, molto dettagliato

### DeepSeek R1 Zero
**Nome API**: `deepseek/deepseek-r1-zero:free`
- **Velocità**: Lenta
- **Context**: 64K token
- **Multilingua**: Buono
- **Note**: Versione sperimentale con ragionamento

### DeepSeek R1 Distill Llama (70B)
**Nome API**: `deepseek/deepseek-r1-distill-llama-70b:free`
- **Velocità**: Media
- **Context**: 128K token
- **Multilingua**: Ottimo
- **Note**: Versione distillata più veloce

### DeepSeek R1 Distill Qwen (32B)
**Nome API**: `deepseek/deepseek-r1-distill-qwen-32b:free`
- **Velocità**: Media-Alta
- **Context**: 64K token
- **Multilingua**: Buono
- **Note**: Versione compatta e veloce

### Nvidia Llama 3.1 Nemotron Ultra
**Nome API**: `nvidia/llama-3.1-nemotron-ultra-253b-v1:free`
- **Velocità**: Media
- **Context**: 128K token
- **Multilingua**: Ottimo
- **Note**: 253B parametri, molto potente

---

## 🎯 MODELLI MULTIMODALI E SPECIALIZZATI

### Google Gemini 2.5 Pro Exp
**Nome API**: `google/gemini-2.5-pro-exp-03-25:free`
- **Velocità**: Media
- **Context**: 1M token
- **Multilingua**: Eccellente
- **Note**: Multimodale avanzato (testo, immagini, PDF)

### Google Gemini 2.0 Flash Exp
**Nome API**: `google/gemini-2.0-flash-exp:free`
- **Velocità**: Molto Alta
- **Context**: 1M token
- **Multilingua**: Eccellente
- **Note**: Versione veloce multimodale

### Google Gemini 2.0 Flash Thinking
**Nome API**: `google/gemini-2.0-flash-thinking-exp:free`
- **Velocità**: Media
- **Context**: 1M token
- **Multilingua**: Eccellente
- **Note**: Con capacità di ragionamento

### Qwen QwQ (32B)
**Nome API**: `qwen/qwq-32b:free`
- **Velocità**: Media
- **Context**: 32K token
- **Multilingua**: Buono
- **Note**: Modello cinese con buone capacità multilingua

---

## 🔄 ROUTER AUTOMATICO

### OpenRouter Free Router
**Nome API**: `openrouter/free`
- **Velocità**: Variabile
- **Context**: Variabile
- **Multilingua**: Variabile
- **Note**: Seleziona automaticamente un modello gratuito casuale

---

## 💡 Raccomandazioni per Chat Multilingua Europea

### Per velocità massima:
1. `google/gemma-3-12b-it:free`
2. `google/gemini-2.0-flash-exp:free`

### Per qualità massima:
1. `meta-llama/llama-3.3-70b-instruct:free`
2. `nvidia/llama-3.1-nemotron-ultra-253b-v1:free`

### Bilanciamento velocità/qualità:
1. `google/gemini-2.0-flash-exp:free`
2. `google/gemma-3-27b-it:free`

---

## 📌 Note Importanti

- Tutti i modelli con `:free` vanno specificati esattamente così nell'API
- Tutti supportano bene italiano, francese, tedesco e spagnolo
- I rate limits possono variare per modello
- **Privacy**: I modelli DeepSeek loggano tutti i prompt (server in Cina)
- Per usare i modelli gratuiti devi abilitare **'Model Training'** nelle impostazioni privacy
- La lista dei modelli gratuiti può cambiare nel tempo

---

📅 **Documento generato il**: 11 Febbraio 2026  
🔗 **Per gli aggiornamenti visita**: https://openrouter.ai/models
