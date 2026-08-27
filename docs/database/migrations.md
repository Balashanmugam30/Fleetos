# Fleetos Database Migrations & Reproducibility Guide

Product: **Fleetos**

---

## Migration Architecture

Fleetos uses SQLAlchemy 2.x declarative metadata and Alembic for reproducible migrations across SQLite (local development/test) and PostgreSQL/Supabase (production).

### Applying Schema & Migrations

```bash
# Initialize / Sync schema automatically via FastAPI startup or script
python -c "import asyncio; from services.api.app.db.database import init_db; asyncio.run(init_db())"
```

### Seeding Baseline Dataset

```bash
# Run canonical demo database seeder
python scripts/seed_database.py
```
