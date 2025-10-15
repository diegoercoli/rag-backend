# FILE 12: app/main.py (Entry Point)
# ============================================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.api.v1 import experiments, configurations, queries, datasets, documents, embeddings, rankings, metrics

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add all routers
app.include_router(experiments.router, prefix=f"{settings.api_prefix}/experiments", tags=["experiments"])
app.include_router(configurations.router, prefix=f"{settings.api_prefix}/configurations", tags=["configurations"])
app.include_router(queries.router, prefix=f"{settings.api_prefix}/queries", tags=["queries"])
app.include_router(datasets.router, prefix=f"{settings.api_prefix}/datasets", tags=["datasets"])
app.include_router(documents.router, prefix=f"{settings.api_prefix}/documents", tags=["documents"])
app.include_router(embeddings.router, prefix=f"{settings.api_prefix}/embeddings", tags=["embeddings"])
app.include_router(rankings.router, prefix=f"{settings.api_prefix}/rankings", tags=["rankings"])
app.include_router(metrics.router, prefix=f"{settings.api_prefix}/metrics", tags=["metrics"])

@app.get("/")
async def root():
    return {
        "message": "RAG Experiment API",
        "version": settings.api_version,
        "docs": f"{settings.api_prefix}/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": settings.api_version}

# Run with: uvicorn app.main:app --reload

# ============================================================================
