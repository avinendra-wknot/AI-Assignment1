### What is this?

A small experiment to see how Ollama decoding settings change the text a local LLM produces. I used the same prompt every time and only changed generation parameters.

Model: `llama3.2` (Ollama 0.33.3)

### Parameters tested

- temperature
- top_p
- top_k
- repeat_penalty (Ollama's repetition control)
- num_predict (max output tokens)
- structured JSON output (`format` + a JSON schema)

Ollama also has `frequency_penalty`, but the usual setting in the docs is `repeat_penalty`, so that is what I used. They are not the same thing: `repeat_penalty` scales the chance of tokens that already appeared, while `frequency_penalty` is a separate penalty based on how often a token has been used.

### Setup

```
ollama pull llama3.2
pip install -r requirements.txt
```

Ollama needs to be running locally (`http://127.0.0.1:11434`).

### Run

```
python experiment.py
python structured_output.py
```

### What I learned

- **temperature** — Lowering it did not make two runs match in this experiment (I did not set a seed). Raising it changed names and details, but the ideas still clustered around similar products.
- **top_p** — Changing it from 0.9 to 0.3 gave a different product in this single run. I cannot say more than that from one sample.
- **top_k** — Changing it from 40 to 5 also gave a different product here. Again, one sample is not enough to describe a general rule.
- **repeat_penalty** — None of the default runs were looping badly, so raising it from 1.1 to 1.5 did not show a clear “less repetition” effect.
- **num_predict** — This one was obvious. 40 tokens cut the answer off mid-sentence. Even 250 tokens still hit the limit (`done_reason: length`).
- **determinism vs creativity** — Low temperature alone was not enough for a repeatable answer. For something closer to deterministic, you would also fix `seed` and use a very low temperature.
- **structured output** — Asking for JSON with a schema made the reply easy to parse with `json.loads`. That is much easier to use in code than free text.
