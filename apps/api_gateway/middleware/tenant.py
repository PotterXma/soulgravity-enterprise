from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from libs.infra_db.base import tenant_context

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = request.headers.get("X-Tenant-ID")
        
        # For health checks and metrics, we might skip tenant check
        if request.url.path in ["/healthz", "/readyz", "/docs", "/openapi.json", "/health"]:
             return await call_next(request)

        if not tenant_id:
            return JSONResponse(
                status_code=400,
                content={"detail": "Missing X-Tenant-ID header"}
            )
            
        token = tenant_context.set(tenant_id)
        try:
            response = await call_next(request)
            return response
        finally:
            tenant_context.reset(token)
