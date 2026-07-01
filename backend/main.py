from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3, os, uuid

DB = os.path.join(os.path.dirname(__file__), "awards.db")

app = FastAPI(title="DnB Awards Spain 2026")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            orden INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS nominaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            artista TEXT NOT NULL,
            track TEXT,
            descripcion TEXT,
            imagen TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        );
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nominacion_id INTEGER NOT NULL,
            voter_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nominacion_id) REFERENCES nominaciones(id)
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_voto_unico ON votos(nominacion_id, voter_hash);
    """)
    # Seed categories if empty
    cur = conn.execute("SELECT COUNT(*) FROM categorias")
    if cur.fetchone()[0] == 0:
        cats = [
            ("Mejor DJ Nacional", "DJ español que más ha roto en 2026", 1),
            ("Mejor Productor", "Productor nacional con mejores releases", 2),
            ("Mejor Track del Año", "Tema que ha marcado el 2026", 3),
            ("Mejor Remix", "Remix que superó al original", 4),
            ("Mejor MC / Vocalista", "Voz que define la escena", 5),
            ("Mejor Festival / Evento", "La mejor experiencia DnB en España", 6),
            ("Mejor Sello", "Label que mueve la escena", 7),
            ("Revelación / Newcomer", "Talento nuevo del año", 8),
            ("Mejor Colaboración", "Colab que hizo historia", 9),
            ("Premio Especial del Público", "El favorito de la gente", 10),
        ]
        conn.executemany("INSERT INTO categorias (nombre, descripcion, orden) VALUES (?,?,?)", cats)
    conn.commit()
    conn.close()

init_db()

# --- SCHEMAS ---
class VotoIn(BaseModel):
    nominacion_id: int
    voter_hash: str

class NominacionIn(BaseModel):
    categoria_id: int
    artista: str
    track: Optional[str] = None
    descripcion: Optional[str] = None

# --- ENDPOINTS ---
@app.get("/api/categorias")
def listar_categorias():
    conn = get_db()
    rows = conn.execute("SELECT * FROM categorias ORDER BY orden").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/nominaciones/{categoria_id}")
def nominaciones_por_categoria(categoria_id: int):
    conn = get_db()
    rows = conn.execute("""
        SELECT n.*, COALESCE(v.votos, 0) as votos
        FROM nominaciones n
        LEFT JOIN (SELECT nominacion_id, COUNT(*) as votos FROM votos GROUP BY nominacion_id) v
        ON n.id = v.nominacion_id
        WHERE n.categoria_id = ?
        ORDER BY votos DESC
    """, (categoria_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/votar")
def votar(v: VotoIn):
    conn = get_db()
    try:
        conn.execute("INSERT INTO votos (nominacion_id, voter_hash) VALUES (?,?)",
                     (v.nominacion_id, v.voter_hash))
        conn.commit()
        conn.close()
        return {"ok": True}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(400, "Ya has votado esta categoría")

@app.get("/api/resultados")
def resultados():
    conn = get_db()
    rows = conn.execute("""
        SELECT c.nombre as categoria, n.artista, n.track, COUNT(v.id) as votos
        FROM nominaciones n
        JOIN categorias c ON n.categoria_id = c.id
        LEFT JOIN votos v ON n.id = v.nominacion_id
        GROUP BY n.id
        ORDER BY c.orden, votos DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/nominaciones")
def crear_nominacion(n: NominacionIn):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO nominaciones (categoria_id, artista, track, descripcion) VALUES (?,?,?,?)",
        (n.categoria_id, n.artista, n.track, n.descripcion)
    )
    conn.commit()
    conn.close()
    return {"id": cur.lastrowid}

@app.get("/api/seed")
def seed_nominaciones():
    """Carga nominaciones de ejemplo para pruebas"""
    conn = get_db()
    samples = [
        (1, "DJ Chapas", None, "Referente del DnB nacional"),
        (1, "Kursiva", None, "15 años de carrera, neurofunk"),
        (1, "Doktor", None, "DJ residente en las mejores noches"),
        (2, "Miklo", None, "Productor con sonido propio"),
        (2, "Mägo", None, "Fusión de DnB con sonidos ibéricos"),
        (3, "DJ Chapas - Tierra", "Tierra", "Himno del 2026"),
        (3, "Kursiva - Córdoba", "Córdoba", "Neurofunk de exportación"),
        (4, "Estepario Challenge RMX", None, "Metal meets DnB"),
        (4, "Remix de Ojos de Brujo", None, "Flamenco-dnb fusion"),
        (5, "Sr. Wilson", None, "MC de referencia"),
        (5, "Rapsusklei", None, "Veterano del hip hop, ahora DnB"),
        (6, "DnB Allstars Mallorca", None, "Weekender de referencia"),
        (6, "Jungle Fest Madrid", None, "El festival que crece cada año"),
        (7, "Kill The Chivato Records", None, "Sello independiente nacional"),
        (7, "Liquid Drops", None, "Sello de liquid funk"),
        (8, "Nueva Promesa", None, "Talento revelación 2026"),
        (8, "Beatriz DnB", None, "DJ revelación femenina"),
        (9, "Chapas x Kursiva", None, "Colaboración que la rompió"),
        (9, "Miklo x Mägo", None, "Dos prodigios juntos"),
        (10, "Premio del Público", None, "El favorito de la escena"),
    ]
    conn.executemany(
        "INSERT INTO nominaciones (categoria_id, artista, track, descripcion) VALUES (?,?,?,?)",
        samples
    )
    conn.commit()
    conn.close()
    return {"ok": True, "insertadas": len(samples)}
