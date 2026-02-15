import structlog
import uuid
import logging
import sys
from contextvars import ContextVar
from typing import Optional

# ContextVar to store correlation_id (trace_id)
correlation_id_ctx: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

def get_correlation_id() -> str:
    """Get current correlation ID or generate a new one if missing."""
    val = correlation_id_ctx.get()
    if not val:
        val = str(uuid.uuid4())
        correlation_id_ctx.set(val)
    return val

def configure_logging(level: str = "INFO", json_format: bool = True):
    """
    Configure structlog and standard logging.
    """
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # Add correlation_id to all logs
    def add_correlation_id(logger, method_name, event_dict):
        cid = correlation_id_ctx.get()
        if cid:
            event_dict["correlation_id"] = cid
        return event_dict

    shared_processors.insert(0, add_correlation_id)

    if json_format:
        formatter = structlog.processors.JSONRenderer()
    else:
        formatter = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard logging to use structlog formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[formatter],
    ))
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level.upper())
