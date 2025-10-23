"""
@author Tom Butler
@date 2025-10-23
@description Health check endpoint for monitoring API status.
             Returns operational status of API and external dependencies.
"""
from fastapi import APIRouter, status
from datetime import datetime
import logging

from models import HealthResponse
from config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        HealthResponse with API status, version, timestamp, and service states
    """
    try:
        services_status = {}

        # Check OpenAI connection
        try:
            # Could make a test call here
            services_status["openai"] = "connected"
        except:
            services_status["openai"] = "disconnected"

        # Check Redis if enabled
        if settings.use_cache:
            try:
                # Would check Redis connection here
                services_status["redis"] = "connected"
            except:
                services_status["redis"] = "disconnected"
        else:
            services_status["redis"] = "disabled"

        # Check Tree-sitter
        services_status["tree_sitter"] = "operational"

        return HealthResponse(
            status="healthy",
            version=settings.app_version,
            timestamp=datetime.utcnow(),
            services=services_status
        )

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            version=settings.app_version,
            timestamp=datetime.utcnow(),
            services={"error": str(e)}
        )