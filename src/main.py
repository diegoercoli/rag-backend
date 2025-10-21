import src.models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.api.v1 import experiments, configurations, queries, datasets, documents, embeddings, rankings, metrics, \
    blacklist, chunking, chunks, preprocessing, query_enhancement, reranking, research_strategies, vector_db, \
    knowledge_base

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

# Register all routers
app.include_router(
    experiments.router,
    prefix=f"{settings.api_prefix}/experiments",
    tags=["experiments"]
)
app.include_router(
    configurations.router,
    prefix=f"{settings.api_prefix}/configurations",
    tags=["configurations"]
)
app.include_router(
    queries.router,
    prefix=f"{settings.api_prefix}/queries",
    tags=["queries"]
)
app.include_router(
    datasets.router,
    prefix=f"{settings.api_prefix}/datasets",
    tags=["datasets"]
)
app.include_router(
    documents.router,
    prefix=f"{settings.api_prefix}/documents",
    tags=["documents"]
)
app.include_router(
    embeddings.router,
    prefix=f"{settings.api_prefix}/embeddings",
    tags=["embeddings"]
)
app.include_router(
    rankings.router,
    prefix=f"{settings.api_prefix}/rankings",
    tags=["rankings"]
)
app.include_router(
    metrics.router,
    prefix=f"{settings.api_prefix}/metrics",
    tags=["metrics"]
)
app.include_router(
    blacklist.router,
    prefix=f"{settings.api_prefix}/blacklist",
    tags=["blacklist"]
)
app.include_router(
    chunking.router,
    prefix=f"{settings.api_prefix}/chunking",
    tags=["chunking"]
)
app.include_router(
    chunks.router,
    prefix=f"{settings.api_prefix}/chunks",
    tags=["chunks"]
)
app.include_router(
    preprocessing.router,
    prefix=f"{settings.api_prefix}/preprocessing",
    tags=["preprocessing"]
)
app.include_router(
    query_enhancement.router,
    prefix=f"{settings.api_prefix}/query-enhancement",
    tags=["query-enhancement"]
)
app.include_router(
    reranking.router,
    prefix=f"{settings.api_prefix}/reranking",
    tags=["reranking"]
)
app.include_router(
    research_strategies.router,
    prefix=f"{settings.api_prefix}/research-strategies",
    tags=["research-strategies"]
)
app.include_router(
    vector_db.router,
    prefix=f"{settings.api_prefix}/vector-db",
    tags=["vector-db"]
)
app.include_router(
    knowledge_base.router,
    prefix=f"{settings.api_prefix}/knowledge-bases",
    tags=["knowledge-bases"]
)

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
