from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apps.api_gateway.middleware.tenant import TenantMiddleware
from apps.api_gateway.middleware.correlation import CorrelationMiddleware
from apps.api_gateway.routers import health, xhs
from libs.core_kernel.plugin_loader import PluginManager
from libs.telemetry import configure_logging
import structlog

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Configure logging & Discover plugins
    configure_logging()
    logger.info("Starting SoulGravity Enterprise...", component="api_gateway")
    PluginManager.instance().discover()
    yield
    # Shutdown
    logger.info("Shutting down...", component="api_gateway")

app = FastAPI(
    title="Lingxi · SoulGravity Enterprise",
    version="0.1.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationMiddleware)
app.add_middleware(TenantMiddleware)

# Routes
from apps.api_gateway.routers import health, xhs
app.include_router(health.router)
app.include_router(xhs.router, prefix="/api/v1")
@app.get("/healthz")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/plugins")
async def list_plugins():
    pm = PluginManager.instance()
    return {"loaded_platforms": pm.list_platforms()}
