"""Operaciones de base de datos JSON."""

import json
from datetime import datetime
from pathlib import Path
from typing import Union

from .models import ShortcutsDatabase


def load_database(db_path: Union[str, Path]) -> ShortcutsDatabase:
    """Carga la base de datos desde JSON.

    Args:
        db_path: Ruta al archivo JSON

    Returns:
        Instancia de ShortcutsDatabase
    """
    path = Path(db_path).expanduser()

    if not path.exists():
        # Crear base de datos vacía
        path.parent.mkdir(parents=True, exist_ok=True)
        database = ShortcutsDatabase()
        save_database(database, db_path)
        return database

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # Convertir strings de datetime a objetos datetime
    if "last_updated" in data and isinstance(data["last_updated"], str):
        data["last_updated"] = datetime.fromisoformat(data["last_updated"])

    return ShortcutsDatabase.model_validate(data)


def save_database(database: ShortcutsDatabase, db_path: Union[str, Path]) -> None:
    """Guarda la base de datos a JSON.

    Args:
        database: Base de datos a guardar
        db_path: Ruta al archivo JSON
    """
    path = Path(db_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    # Actualizar timestamp
    database.last_updated = datetime.now()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            database.model_dump(),
            f,
            indent=2,
            ensure_ascii=False,
            default=lambda x: x.isoformat() if isinstance(x, datetime) else x,
        )
