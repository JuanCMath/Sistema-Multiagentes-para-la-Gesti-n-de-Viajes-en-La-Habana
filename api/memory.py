from fastapi import APIRouter, HTTPException
import json

router = APIRouter()

MEMORY_FILE_PATH = "memory/memory_storage.json"

@router.delete("/reset-memory")
def reset_memory():
    try:
        # Sobrescribe el archivo con un diccionario vacío
        with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)
        return {"detail": "Memory reset successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
