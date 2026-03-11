from __future__ import annotations

import json
from pathlib import Path

from .models import Incident, incident_from_dict


def load_incident(path: str | Path) -> Incident:
    incident_dir = Path(path)
    incident_file = incident_dir / "incident.json"
    with incident_file.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return incident_from_dict(data)


def load_incident_dict(path: str | Path) -> dict:
    incident_dir = Path(path)
    incident_file = incident_dir / "incident.json"
    with incident_file.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_incident_dict(path: str | Path, data: dict) -> None:
    incident_dir = Path(path)
    incident_file = incident_dir / "incident.json"
    with incident_file.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
