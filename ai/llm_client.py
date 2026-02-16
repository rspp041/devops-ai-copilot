import os
from dataclasses import dataclass

@dataclass
class LLMResult:
    text: str

class LLMClient:
    """
    Pluggable client. This repo package implements OpenAI + a mock mode.

    Env:
      - LLM_PROVIDER: "openai" | "mock"
      - OPENAI_API_KEY: required if provider=openai
      - OPENAI_MODEL: optional, defaults to "gpt-5.2"
    """

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "mock").lower()

    def complete(self, prompt: str) -> LLMResult:
        if self.provider == "mock":
            return LLMResult(text=self._mock(prompt))
        if self.provider == "openai":
            return self._openai(prompt)
        raise ValueError(f"Unsupported LLM_PROVIDER: {self.provider}")

    def _mock(self, prompt: str) -> str:
        return (
            "### [MOCK MODE]\n\n"
            "LLM_PROVIDER=mock so no external calls were made.\n\n"
            "Prompt preview:\n\n"
            + prompt[:1200]
            + "\n\n(End mock)"
        )

    def _openai(self, prompt: str) -> LLMResult:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set (use GitHub Secrets or local env).")

        model = os.getenv("OPENAI_MODEL", "gpt-5.2")

        # Official SDK (Responses API)
        # https://developers.openai.com/api/reference/python/ citeturn0search5
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        resp = client.responses.create(
            model=model,
            input=prompt,
        )

        return LLMResult(text=getattr(resp, "output_text", "") or str(resp))
