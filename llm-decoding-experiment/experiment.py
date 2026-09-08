"""
Same prompt, different decoding settings.

This talks to the local Ollama API and prints whatever the model returns.
"""

import ollama

MODEL = "llama3.2"

PROMPT = (
    "Invent a futuristic product that could realistically exist in 2035. "
    "Explain what it does, who would use it, how it works, and what problem it solves."
)

configs = [
    {
        "name": "low temperature",
        "runs": 2,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_predict": 250,
        },
        "changed": "temperature only (low / more deterministic)",
    },
    {
        "name": "medium temperature",
        "runs": 1,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_predict": 250,
        },
        "changed": "temperature only (balanced)",
    },
    {
        "name": "high temperature",
        "runs": 3,
        "options": {
            "temperature": 1.3,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_predict": 250,
        },
        "changed": "temperature only (higher / more random). Run 3 times.",
    },
    {
        "name": "low top_p",
        "runs": 1,
        "options": {
            "temperature": 0.7,
            "top_p": 0.3,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_predict": 250,
        },
        "changed": "top_p only (0.3 instead of 0.9). Temperature matches the medium run.",
    },
    {
        "name": "low top_k",
        "runs": 1,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 5,
            "repeat_penalty": 1.1,
            "num_predict": 250,
        },
        "changed": "top_k only (5 instead of 40). Temperature matches the medium run.",
    },
    {
        "name": "higher repeat_penalty",
        "runs": 1,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.5,
            "num_predict": 250,
        },
        "changed": "repeat_penalty only (1.5 instead of 1.1). This is Ollama's repetition control.",
    },
    {
        "name": "short max tokens", 
        "runs": 1,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_predict": 40,
        },
        "changed": "num_predict only (40 instead of 250). This is the output length cap.",
    },
]


def run_one(name, options, run_number, total_runs, changed):
    print("=" * 72)
    print(f"Configuration: {name}  (run {run_number}/{total_runs})")
    print(f"Changed: {changed}")
    print(f"Options: {options}")
    print("-" * 72)

    result = ollama.generate(
        model=MODEL,
        prompt=PROMPT,
        options=options,
    )

    text = result.response
    tokens = result.eval_count
    done_reason = result.done_reason

    print(text)
    print("-" * 72)
    print(f"tokens generated: {tokens}  |  done_reason: {done_reason}")
    print()

    return {
        "name": name,
        "run": run_number,
        "options": options,
        "changed": changed,
        "output": text,
        "tokens": tokens,
        "done_reason": done_reason,
    }


def main():
    print(f"Model: {MODEL}")
    print("Prompt (same for every run):")
    print(PROMPT)
    print()

    all_results = []

    for config in configs:
        for i in range(config["runs"]):
            one = run_one(
                name=config["name"],
                options=config["options"],
                run_number=i + 1,
                total_runs=config["runs"],
                changed=config["changed"],
            )
            all_results.append(one)

    # Save a plain-text copy so results.md can be filled in from real outputs.
    with open("raw_outputs.txt", "w", encoding="utf-8") as f:
        f.write(f"Model: {MODEL}\n")
        f.write(f"Prompt: {PROMPT}\n\n")
        for r in all_results:
            f.write("=" * 72 + "\n")
            f.write(f"Configuration: {r['name']}  (run {r['run']})\n")
            f.write(f"Changed: {r['changed']}\n")
            f.write(f"Options: {r['options']}\n")
            f.write(f"tokens generated: {r['tokens']}  |  done_reason: {r['done_reason']}\n")
            f.write("-" * 72 + "\n")
            f.write(r["output"] + "\n\n")

    print("Saved all outputs to raw_outputs.txt")


if __name__ == "__main__":
    main()
