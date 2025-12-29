from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    base_url: str
    model: str
    timeout_s: int = 120
    max_retries: int = 2


class LLMError(RuntimeError):
    pass


def load_llm_config() -> LLMConfig:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise LLMError("OPENAI_API_KEY is required")

    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-5.2-mini").strip()
    return LLMConfig(api_key=api_key, base_url=base_url, model=model)


def chat_completion(*, system: str, user: str, temperature: float = 0.0) -> str:
    cfg = load_llm_config()
    url = f"{cfg.base_url}/chat/completions"

    payload = {
        "model": cfg.model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }

    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }

    last_err: Exception | None = None
    for attempt in range(cfg.max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=cfg.timeout_s)
            if resp.status_code >= 400:
                raise LLMError(f"HTTP {resp.status_code}: {resp.text[:2000]}")
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            if attempt >= cfg.max_retries:
                break
            time.sleep(1.5 * (attempt + 1))

    raise LLMError(f"LLM request failed: {last_err}")
