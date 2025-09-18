from fastapi import APIRouter, HTTPException, status
import logging

from models import AnalysisRequest, AnalysisResponse, ErrorResponse
from services import CodeAnalyzerService
from config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize service
analyzer_service = CodeAnalyzerService()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def analyze_code(request: AnalysisRequest):
    """Analyze code for syntax, complexity, and quality"""
    try:
        logger.info(f"Analyzing {request.language.value} code")

        # Perform analysis
        analysis_result = analyzer_service.analyze_code(request)

        # Extract metrics or use defaults
        metrics = analysis_result.get("metrics")

        # Calculate performance score based on complexity
        if metrics:
            complexity = metrics.cyclomatic_complexity
            readability = metrics.readability_score
            lines_of_code = metrics.lines_of_code
        else:
            complexity = 1
            readability = 85.0
            lines_of_code = 0

        performance_score = max(0, min(100, 100 - (complexity * 5)))  # Simple heuristic

        logger.debug(f"Analysis result: valid={analysis_result.get('valid')}, complexity={complexity}")

        return AnalysisResponse(
            syntax_valid=analysis_result.get("valid", True),
            language=request.language.value,
            complexity=complexity,
            readability_score=readability,
            performance_score=performance_score,
            lines_of_code=lines_of_code,
            syntax_errors=analysis_result.get("issues", []),
            suggestions=analysis_result.get("suggestions", []),
            metrics=metrics,
            formatted_code=analysis_result.get("formatted_code"),
            ast_structure=analysis_result.get("ast_structure")
        )

    except ValueError as e:
        logger.error(f"Code analysis validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request data: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Code analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code analysis failed: {str(e)}"
        )


@router.post(
    "/analyze/format",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def format_code(request: AnalysisRequest):
    """Format code according to language standards"""
    try:
        logger.info(f"Formatting {request.language.value} code")
        logger.debug(f"Format request: language={request.language.value}, code_length={len(request.code)}")

        # Create a modified request with format_code=True
        format_request = AnalysisRequest(
            code=request.code,
            language=request.language,
            check_syntax=False,
            check_complexity=False,
            suggest_improvements=False,
            format_code=True
        )

        analysis_result = analyzer_service.analyze_code(format_request)

        if not analysis_result.get("formatted_code"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not format code"
            )

        return {
            "formatted_code": analysis_result["formatted_code"],
            "language": request.language.value
        }

    except Exception as e:
        logger.error(f"Code formatting failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code formatting failed: {str(e)}"
        )


@router.post(
    "/analyze/validate",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def validate_syntax(request: AnalysisRequest):
    """Validate code syntax"""
    try:
        logger.info(f"Validating {request.language.value} code syntax")

        # Create a modified request with only syntax checking
        validate_request = AnalysisRequest(
            code=request.code,
            language=request.language,
            check_syntax=True,
            check_complexity=False,
            suggest_improvements=False,
            format_code=False
        )

        analysis_result = analyzer_service.analyze_code(validate_request)

        return {
            "valid": analysis_result["valid"],
            "language": request.language.value,
            "issues": analysis_result.get("issues", [])
        }

    except Exception as e:
        logger.error(f"Syntax validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Syntax validation failed: {str(e)}"
        )