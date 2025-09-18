from fastapi import FastAPI

from app.core.config import get_settings
from app.core.errors import init_error_handlers
from app.core.logging import configure_logging
from app.middleware.request_id import RequestIDMiddleware
from app.version import VERSION


def create_app() -> FastAPI:
    cfg = get_settings()
    configure_logging(service=cfg.service_name, env=cfg.env, level=cfg.log_level)

    app = FastAPI(
        title=cfg.service_name,
        version=VERSION,
        docs_url="/docs",
    )

    app.add_middleware(RequestIDMiddleware)

    init_error_handlers(app)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": cfg.service_name, "version": VERSION}

    return app


app = create_app()
