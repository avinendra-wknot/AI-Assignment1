"""
Same product idea, but ask the model to answer in JSON.

Ollama can take a JSON schema in the `format` field. After it replies,
we parse the text with Python's json module. If it is not valid JSON,
we just report that — we do not try to "fix" it.
"""

import json
import ollama

MODEL = "llama3.2"

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "problem": {"type": "string"},
        "target_users": {"type": "string"},
        "how_it_works": {"type": "string"},
        "key_feature": {"type": "string"},
    },
    "required": [
        "name",
        "problem",
        "target_users",
        "how_it_works",
        "key_feature",
    ],
}

PROMPT = (
    "Invent a futuristic product that could realistically exist in 2035. "
    "Return JSON only, with these fields: "
    "name, problem, target_users, how_it_works, key_feature."
)


def main():
    print("Model:", MODEL)
    print("Prompt:", PROMPT)
    print("Schema:", json.dumps(SCHEMA, indent=2))
    print("-" * 72)

    result = ollama.generate(
        model=MODEL,
        prompt=PROMPT,
        format=SCHEMA,
        options={
            "temperature": 0.2,
            "num_predict": 300,
        },
    )

    raw = result.response
    print("Raw model output:")
    print(raw)
    print("-" * 72)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as err:
        print("JSON validation: FAILED")
        print("The model did not return valid JSON.")
        print("Error:", err)
        return

    print("JSON validation: OK (json.loads succeeded)")
    print("Parsed fields:")
    for key in SCHEMA["required"]:
        value = data.get(key, "<missing>")
        print(f"  {key}: {value}")

    missing = [key for key in SCHEMA["required"] if key not in data]
    extra = [key for key in data if key not in SCHEMA["properties"]]
    if missing:
        print("Missing required fields:", missing)
    if extra:
        print("Extra fields:", extra)


if __name__ == "__main__":
    main()
