import json
from typing import Any, Dict, List, Optional
from llama_cpp import Llama

class LLMClient:
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 2048,
        n_threads: int = 16,
        temperature: float = 0.5,
        verbose: bool = False,
    ):
        self.temperature = temperature
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=verbose,
        )

    def complete(self, prompt: str, max_tokens: int = 256, stop: Optional[List[str]] = None) -> str:
        resp = self.llm.create_completion(
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=max_tokens,
            stop=stop or ["</s>"],
        )
        return resp["choices"][0]["text"]

    def complete_json(self, prompt: str, max_tokens: int = 256, stop: Optional[List[str]] = None) -> Dict[str, Any]:
        text = self.complete(prompt, max_tokens=max_tokens, stop=stop).strip()
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1]
        try:
            return json.loads(text)
        except Exception:
            return {"location": None, "reason": "non-json-output", "raw": text}
