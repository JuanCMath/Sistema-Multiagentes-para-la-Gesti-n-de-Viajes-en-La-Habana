from google.adk.sessions import InMemorySessionService
from memory.memory_service import JsonMemoryService

session_service = InMemorySessionService()
memory_service = JsonMemoryService("src/memory/memory_storage.json")