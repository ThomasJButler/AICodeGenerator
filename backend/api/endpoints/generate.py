from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List
import uuid
import time
import logging
import asyncio

from models import (
    GenerationRequest,
    GenerationResponse,
    BatchGenerationRequest,
    GenerationStatus,
    ErrorResponse
)
from services import CodeGeneratorService
from config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize service
generator_service = CodeGeneratorService()


@router.post(
    "/generate",
    response_model=GenerationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def generate_code(request: GenerationRequest):
    """Generate code based on the provided prompt"""
    generation_id = f"gen_{uuid.uuid4().hex[:8]}"
    start_time = time.time()

    try:
        logger.info(f"Starting generation {generation_id} for {request.programming_language.value}")

        # Generate code
        code = await generator_service.generate_code(request)

        # Generate tests if requested
        tests = None
        if request.include_tests:
            tests = await generator_service.generate_tests(code, request)

        # Generate documentation if requested
        documentation = None
        if request.include_docs:
            documentation = await generator_service.generate_documentation(code, request)

        # Calculate metrics
        metrics = await generator_service.calculate_metrics(code, request.programming_language.value)

        processing_time = time.time() - start_time

        return GenerationResponse(
            id=generation_id,
            status=GenerationStatus.COMPLETED,
            code=code,
            language=request.programming_language.value,
            tests=tests,
            documentation=documentation,
            metrics=metrics,
            processing_time=round(processing_time, 2)
        )

    except Exception as e:
        logger.error(f"Generation {generation_id} failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code generation failed: {str(e)}"
        )


@router.post(
    "/generate/batch",
    response_model=List[GenerationResponse],
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def generate_batch(batch_request: BatchGenerationRequest):
    """Generate multiple code snippets concurrently (max 3)"""
    try:
        if len(batch_request.requests) > settings.max_concurrent_generations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Maximum {settings.max_concurrent_generations} concurrent generations allowed"
            )

        # Process all requests concurrently
        tasks = []
        for request in batch_request.requests:
            tasks.append(generate_code_async(request))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch generation {i} failed: {str(result)}")
                responses.append(
                    GenerationResponse(
                        id=f"gen_{uuid.uuid4().hex[:8]}",
                        status=GenerationStatus.FAILED,
                        language=batch_request.requests[i].programming_language.value,
                        error=str(result)
                    )
                )
            else:
                responses.append(result)

        return responses

    except Exception as e:
        logger.error(f"Batch generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch generation failed: {str(e)}"
        )


async def generate_code_async(request: GenerationRequest) -> GenerationResponse:
    """Async helper for batch generation"""
    generation_id = f"gen_{uuid.uuid4().hex[:8]}"
    start_time = time.time()

    try:
        # Generate code
        code = await generator_service.generate_code(request)

        # Generate tests if requested
        tests = None
        if request.include_tests:
            tests = await generator_service.generate_tests(code, request)

        # Generate documentation if requested
        documentation = None
        if request.include_docs:
            documentation = await generator_service.generate_documentation(code, request)

        # Calculate metrics
        metrics = await generator_service.calculate_metrics(code, request.programming_language.value)

        processing_time = time.time() - start_time

        return GenerationResponse(
            id=generation_id,
            status=GenerationStatus.COMPLETED,
            code=code,
            language=request.programming_language.value,
            tests=tests,
            documentation=documentation,
            metrics=metrics,
            processing_time=round(processing_time, 2)
        )

    except Exception as e:
        return GenerationResponse(
            id=generation_id,
            status=GenerationStatus.FAILED,
            language=request.programming_language.value,
            error=str(e)
        )


@router.get(
    "/generate/{generation_id}",
    response_model=GenerationResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Generation not found"}
    }
)
async def get_generation(generation_id: str):
    """Get the status and result of a specific generation"""
    # This would typically fetch from a database or cache
    # For now, return a placeholder response
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Generation retrieval not yet implemented"
    )