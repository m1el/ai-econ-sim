# /// script
# dependencies = ["httpx"]
# ///
"""Fan out the AI-economy questionnaire to 10 frontier models via OpenRouter."""
import asyncio, json, os, pathlib, re, sys

import httpx

HERE = pathlib.Path(__file__).parent
QUESTION = (HERE / "question.md").read_text()
OUT = HERE / "responses"
OUT.mkdir(exist_ok=True)

MODELS = [
    "openai/gpt-5.5",
    "anthropic/claude-opus-4.8",
    "google/gemini-3.1-pro-preview",
    "x-ai/grok-4.3",
    "deepseek/deepseek-v4-pro",
    "qwen/qwen3.7-max",
    "moonshotai/kimi-k2.6",
    "z-ai/glm-5.1",
    "minimax/minimax-m3",
    "mistralai/mistral-large-2512",
]

KEY = os.environ["OPENROUTER_API_KEY"]


async def ask(client: httpx.AsyncClient, model: str) -> dict:
    slug = re.sub(r"[^a-z0-9.-]+", "_", model.lower())
    body = {
        "model": model,
        "messages": [{"role": "user", "content": QUESTION}],
        "max_tokens": 8000,
        "temperature": 0.7,
    }
    for attempt in range(3):
        try:
            r = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {KEY}"},
                json=body,
                timeout=600,
            )
            data = r.json()
            if "error" in data:
                raise RuntimeError(data["error"])
            msg = data["choices"][0]["message"]
            text = msg.get("content") or ""
            if not text.strip():
                raise RuntimeError(f"empty content, finish_reason={data['choices'][0].get('finish_reason')}")
            usage = data.get("usage", {})
            (OUT / f"{slug}.md").write_text(f"# {model}\n\n{text}\n")
            print(f"OK   {model}  ({usage.get('completion_tokens')} completion tok)", flush=True)
            return {"model": model, "ok": True, "usage": usage}
        except Exception as e:
            print(f"RETRY {model} attempt {attempt+1}: {e}", flush=True)
            await asyncio.sleep(5 * (attempt + 1))
    print(f"FAIL {model}", flush=True)
    return {"model": model, "ok": False}


async def main():
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[ask(client, m) for m in MODELS])
    (HERE / "summary.json").write_text(json.dumps(results, indent=2))
    fails = [r["model"] for r in results if not r["ok"]]
    print(f"\nDone. {len(MODELS)-len(fails)}/{len(MODELS)} succeeded. Fails: {fails}", flush=True)


asyncio.run(main())
