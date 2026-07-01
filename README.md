# DnB Awards Spain 2026 🏆

## Estructura

```
backend/     → FastAPI + SQLite
frontend/    → Vue 3 + Vite
```

## Arrancar

### Backend
```bash
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend && npm run dev
```

## API
- `GET  /api/categorias` — listar categorías
- `GET  /api/nominaciones/:categoria_id` — nominados por categoría
- `POST /api/votar` — emitir voto
- `GET  /api/resultados` — resultados globales
- `POST /api/nominaciones` — crear nominación (admin)
