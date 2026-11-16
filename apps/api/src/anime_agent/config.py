"""Paths can be configured without depending on sibling repositories."""
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def project_path(variable: str, default: str) -> Path:
    value = Path(os.environ.get(variable, default)).expanduser()
    return value.resolve() if value.is_absolute() else (ROOT / value).resolve()


@dataclass(frozen=True)
class Settings:
    dataset_path: Path
    conversation_db: Path

    @classmethod
    def from_environment(cls):
        return cls(
            dataset_path=project_path("ANIME_DATASET_PATH", "data/processed/current.json"),
            conversation_db=project_path("ANIME_CONVERSATION_DB", "data/conversations.sqlite3"),
        )
