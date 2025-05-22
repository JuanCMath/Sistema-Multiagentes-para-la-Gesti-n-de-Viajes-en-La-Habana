# Sistema Multiagentes para la Gestión de Viajes en La Habana

Sistema multiagentes utilizando [Google ADK (Agent Development Kit)](https://github.com/google/adk) que facilita la gestión de los viajes del usuario por La Habana, teniendo en cuenta las condiciones climáticas vigentes.

---

## Requerimientos

- **Sistema Operativo:** Windows, Linux (recomendado Linux)
- **Lenguaje:** Python 3.10 o superior
- **Dependencias:** Listadas en `requirements.txt` (ver abajo)
- **API Key:** Necesitas una clave de API de Google para usar Google Generative AI [Obtener API KEY](https://aistudio.google.com/app/apikey)

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/JuanCMath/Sistema-Multiagentes-para-la-Gesti-n-de-Viajes-en-La-Habana.git
   cd Sistema-Multiagentes-para-la-Gesti-n-de-Viajes-en-La-Habana
   ```
2. **Selecciona la rama main:**
   ```bash
   git checkout main
   ```
3. **Crea un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Configura variables de entorno:**
   - Crea un archivo `.env` con tu clave de API de Google:
     ```
     GOOGLE_API_KEY= tu_clave_aqui
     ```

## Ejecución

Para iniciar el servidor:

```bash
uvicorn main:app --reload
```

- El sistema levantará una API RESTful en `http://localhost:8000/docs#/default`.

## Uso

### Endpoints principales

- `POST /agent/orquestator`
  - Consulta al agente orquestador con un mensaje del usuario.
  - Ejemplo de payload:
    ```json
    {
      "query": "¿Cuál es la mejor ruta para ir del Vedado al Centro Habana con lluvia?"
    }
    ```

- `POST /viajes/`
  - Crea un nuevo viaje.

- `GET /viajes/`
  - Lista todos los viajes guardados.

- `GET /viajes/{viaje_id}`
  - Obtiene los detalles de un viaje por su ID.

- `PUT /viajes/{viaje_id}`
  - Actualiza un viaje existente.

- `DELETE /viajes/{viaje_id}`
  - Elimina un viaje.

- `DELETE /conversaciones/`
  - Elimina todo el historial de conversaciones.

### Ejemplo de flujo de uso

1. Levanta el servidor.
2. Realiza peticiones a los endpoints usando herramientas como Postman, Insomnia, o `curl`.
3. Consulta al agente y gestiona viajes mediante las rutas descritas arriba.

## Dependencias principales

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Google Generative AI](https://github.com/google/generative-ai-python)
- [Google ADK](https://github.com/google/adk)
- [Alembic](https://alembic.sqlalchemy.org/)

Todas las dependencias están en `requirements.txt`.

## Secciones del sistema

- **Agente Orquestador:** Responde preguntas del usuario y coordina la gestión de viajes.
- **Gestión de Viajes:** CRUD de viajes (crear, listar, actualizar, eliminar).
- **Historial de Conversaciones:** Registra y permite limpiar las conversaciones con el agente.

## Imágenes y ejemplos visuales

---por agregar----
