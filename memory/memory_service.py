import json
import os
from google.adk.memory import BaseMemoryService
from datetime import datetime

class JsonMemoryService(BaseMemoryService):
    def __init__(self, filename="memory.json"):
        self.filename = filename
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.filename):
            if os.path.getsize(self.filename) == 0:
                # Archivo existe pero está vacío, inicializa con lista vacía
                return []
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Archivo corrupto o contenido inválido, resetear memoria
                    return []
        return []


    def _save_memory(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    async def add_session_to_memory(self, session):
        """
        Guarda todos los eventos de la sesión en memoria (archivo JSON).
        Reemplaza el contenido previo con la nueva sesión completa.
        """
        session_data = []

        for event in session.events:
            timestamp = None
            if hasattr(event, "timestamp") and event.timestamp is not None:
                if isinstance(event.timestamp, datetime):
                    timestamp = event.timestamp.isoformat()
                elif isinstance(event.timestamp, (float, int)):
                    timestamp = datetime.fromtimestamp(event.timestamp).isoformat()
                else:
                    timestamp = str(event.timestamp)

            event_dict = {
                "author": event.author,
                "content": [part.text for part in event.content.parts] if event.content else [],
                "timestamp": timestamp,
                "event_type": getattr(event, "event_type", None)
            }
            session_data.append(event_dict)

        self.memory = session_data  # Reemplaza toda la memoria con esta sesión
        self._save_memory()

    async def search_memory(self, app_name, user_id, query):
        """
        Busca el query dentro de los textos guardados y devuelve los eventos encontrados.
        """
        results = []
        query_lower = query.lower()
        for event in self.memory:
            if any(query_lower in text.lower() for text in event.get("content", [])):
                results.append(event)
        return results
    