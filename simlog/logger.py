import json
from datetime import datetime
from pathlib import Path


class SimLogger:
    def __init__(self, root: str = "data/runs"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.run_dir = self.root / timestamp
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.events_file = self.run_dir / "events.jsonl"
        self._file_handle = open(self.events_file, "w", encoding="utf-8")

    def log(self, event: dict) -> None:
        line = json.dumps(event, ensure_ascii=False)
        self._file_handle.write(line + "\n")
        self._file_handle.flush()

    def close(self) -> None:
        if self._file_handle:
            self._file_handle.close()

    def __del__(self):
        self.close()
