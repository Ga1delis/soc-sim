import json
from pathlib import Path
from typing import Dict, Any, List

class MemoryStore:
    def __init__(self, root: str = "data/memory"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, agent_name: str) -> Path:
        return self.root / f"{agent_name}.json"

    def load(self, agent_name: str) -> Dict[str, Any]:
        p = self._path(agent_name)
        if not p.exists():
            return {"summary": "", "facts": []}
        return json.loads(p.read_text(encoding="utf-8"))

    def save(self, agent_name: str, data: Dict[str, Any]) -> None:
        p = self._path(agent_name)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_fact(self, agent_name: str, fact: str, max_facts: int = 50) -> None:
        data = self.load(agent_name)
        facts: List[str] = data.get("facts", [])
        facts.append(fact)
        data["facts"] = facts[-max_facts:]
        self.save(agent_name, data)

