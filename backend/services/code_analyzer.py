"""
@author Tom Butler
@date 2025-10-23
@description Code analysis service using tree-sitter for syntax validation.
             Calculates complexity metrics and generates improvement suggestions.
"""
import logging
from typing import Dict, List, Any, Optional
try:
    import tree_sitter_languages as tsl
    from tree_sitter import Node
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("tree-sitter-languages not available, using fallback analysis")
import black
import autopep8

from models import AnalysisRequest, CodeMetrics

logger = logging.getLogger(__name__)


class CodeAnalyzerService:
    """
    Service for static code analysis and quality metrics.

    Uses tree-sitter for AST parsing and syntax validation.
    Falls back to Python compile() when tree-sitter unavailable.
    """

    def __init__(self):
        self.parsers = {}
        self._init_parsers()

    def _init_parsers(self):
        """
        Initialises tree-sitter parsers for all supported languages.

        Gracefully handles missing parsers and logs warnings.
        """
        if not TREE_SITTER_AVAILABLE:
            logger.warning("Tree-sitter not available, syntax parsing will be limited")
            return

        language_mappings = {
            "python": "python",
            "javascript": "javascript",
            "typescript": "typescript",
            "java": "java",
            "csharp": "c_sharp",
            "go": "go",
            "rust": "rust",
            "cpp": "cpp",
            "ruby": "ruby",
            "swift": "swift"
        }

        for lang, ts_lang in language_mappings.items():
            try:
                self.parsers[lang] = tsl.get_parser(ts_lang)
            except Exception as e:
                logger.warning(f"Could not load parser for {lang}: {e}")

    def analyze_code(self, request: AnalysisRequest) -> Dict[str, Any]:
        """
        Analyses code for syntax validity, complexity, and quality.

        Performs requested checks based on AnalysisRequest flags.
        Returns comprehensive analysis including issues, metrics, and suggestions.

        Args:
            request: Analysis request with code and check flags

        Returns:
            Dictionary containing validation results, issues, metrics, suggestions, AST, formatted code

        Raises:
            Exception: If analysis fails
        """
        try:
            result = {
                "valid": False,
                "issues": [],
                "suggestions": [],
                "metrics": None,
                "ast_structure": None,
                "formatted_code": None
            }

            if request.check_syntax:
                syntax_result = self._check_syntax(request.code, request.language.value)
                result["valid"] = syntax_result["valid"]
                result["issues"].extend(syntax_result.get("issues", []))
                result["ast_structure"] = syntax_result.get("ast")

            if request.check_complexity:
                metrics = self._calculate_metrics(request.code, request.language.value)
                result["metrics"] = metrics

            if request.suggest_improvements:
                suggestions = self._generate_suggestions(
                    request.code,
                    request.language.value,
                    result.get("metrics")
                )
                result["suggestions"] = suggestions

            if request.format_code:
                formatted = self._format_code(request.code, request.language.value)
                result["formatted_code"] = formatted

            return result

        except Exception as e:
            logger.error(f"Code analysis failed: {str(e)}")
            raise

    def _check_syntax(self, code: str, language: str) -> Dict[str, Any]:
        """
        Validates syntax using tree-sitter AST parsing.

        Falls back to Python compile() for Python when tree-sitter unavailable.
        For other languages without tree-sitter, assumes valid syntax.

        Args:
            code: Source code to validate
            language: Programming language identifier

        Returns:
            Dictionary with valid flag, issues list, and AST structure
        """
        result = {"valid": True, "issues": [], "ast": None}

        if not TREE_SITTER_AVAILABLE:
            if language == "python":
                try:
                    compile(code, '<string>', 'exec')
                    result["valid"] = True
                except SyntaxError as e:
                    result["valid"] = False
                    result["issues"].append({
                        "type": "error",
                        "message": f"Syntax error: {str(e)}",
                        "line": e.lineno if e.lineno else None
                    })
            else:
                # For other languages, assume valid syntax
                result["valid"] = True
            return result

        if language not in self.parsers:
            result["issues"].append({
                "type": "error",
                "message": f"Parser not available for {language}"
            })
            return result

        try:
            parser = self.parsers[language]
            tree = parser.parse(bytes(code, "utf8"))
            root = tree.root_node

            # Check for syntax errors
            errors = self._find_syntax_errors(root)
            if errors:
                result["valid"] = False
                result["issues"].extend(errors)

            # Get AST structure
            result["ast"] = self._node_to_dict(root)

            return result

        except Exception as e:
            result["valid"] = False
            result["issues"].append({
                "type": "error",
                "message": f"Parse error: {str(e)}"
            })
            return result

    def _find_syntax_errors(self, node, errors: List[Dict] = None) -> List[Dict]:
        """Recursively find syntax errors in the AST"""
        if not TREE_SITTER_AVAILABLE:
            return []

        if errors is None:
            errors = []

        if node.type == "ERROR" or node.is_missing:
            errors.append({
                "type": "error",
                "line": node.start_point[0] + 1,
                "column": node.start_point[1],
                "message": f"Syntax error at line {node.start_point[0] + 1}"
            })

        for child in node.children:
            self._find_syntax_errors(child, errors)

        return errors

    def _node_to_dict(self, node) -> Dict[str, Any]:
        """Convert Tree-sitter node to dictionary"""
        if not TREE_SITTER_AVAILABLE:
            return {}

        return {
            "type": node.type,
            "start": {"line": node.start_point[0], "column": node.start_point[1]},
            "end": {"line": node.end_point[0], "column": node.end_point[1]},
            "children": [self._node_to_dict(child) for child in node.children if not child.is_extra]
        }

    def _calculate_metrics(self, code: str, language: str) -> CodeMetrics:
        """Calculate code quality metrics"""
        lines = code.split('\n')

        # Lines of code (excluding empty lines and comments)
        loc = self._count_lines_of_code(lines, language)

        # Cyclomatic complexity
        complexity = self._calculate_cyclomatic_complexity(code, language)

        # Readability score
        readability = self._calculate_readability(lines)

        # Complexity estimates
        time_complexity = self._estimate_time_complexity(code)
        memory_complexity = self._estimate_memory_complexity(code)

        return CodeMetrics(
            lines_of_code=loc,
            cyclomatic_complexity=complexity,
            readability_score=readability,
            estimated_execution_time=time_complexity,
            memory_complexity=memory_complexity
        )

    def _count_lines_of_code(self, lines: List[str], language: str) -> int:
        """Count actual lines of code"""
        comment_indicators = {
            "python": ["#"],
            "javascript": ["//", "/*", "*/"],
            "typescript": ["//", "/*", "*/"],
            "java": ["//", "/*", "*/"],
            "csharp": ["//", "/*", "*/"],
            "go": ["//", "/*", "*/"],
            "rust": ["//", "/*", "*/"],
            "cpp": ["//", "/*", "*/"],
            "ruby": ["#"],
            "swift": ["//", "/*", "*/"]
        }

        indicators = comment_indicators.get(language, ["//", "#"])
        loc = 0

        for line in lines:
            stripped = line.strip()
            if stripped and not any(stripped.startswith(ind) for ind in indicators):
                loc += 1

        return loc

    def _calculate_cyclomatic_complexity(self, code: str, language: str) -> int:
        """Calculate cyclomatic complexity"""
        # Decision points that increase complexity
        decision_keywords = [
            "if", "elif", "else", "for", "while", "except",
            "case", "when", "catch", "switch", "&&", "||",
            "?", "try", "rescue", "unless"
        ]

        complexity = 1  # Base complexity

        for keyword in decision_keywords:
            # Simple keyword counting (could be improved with AST)
            complexity += code.count(f" {keyword} ") + code.count(f"\n{keyword} ")

        return complexity

    def _calculate_readability(self, lines: List[str]) -> float:
        """Calculate code readability score"""
        if not lines:
            return 100.0

        total_length = sum(len(line) for line in lines)
        avg_length = total_length / len(lines)

        # Factors affecting readability
        score = 100.0

        # Penalize long lines
        if avg_length > 80:
            score -= min(30, (avg_length - 80) * 0.5)

        # Penalize very short or very long functions
        if len(lines) < 3:
            score -= 10
        elif len(lines) > 50:
            score -= min(20, (len(lines) - 50) * 0.2)

        # Check for proper indentation (simple heuristic)
        indent_issues = sum(1 for line in lines if line and line[0] not in ' \t' and ':' in line)
        score -= min(20, indent_issues * 2)

        return max(0.0, min(100.0, score))

    def _estimate_time_complexity(self, code: str) -> str:
        """Estimate algorithmic time complexity"""
        code_lower = code.lower()

        # Check for nested loops
        loop_keywords = ["for", "while"]
        loop_count = sum(code_lower.count(kw) for kw in loop_keywords)

        if loop_count >= 3:
            return "O(n³) or higher"
        elif loop_count == 2:
            # Check if loops are nested
            lines = code.split('\n')
            indent_levels = []
            for line in lines:
                if any(kw in line for kw in loop_keywords):
                    indent_levels.append(len(line) - len(line.lstrip()))

            if len(indent_levels) >= 2 and indent_levels[1] > indent_levels[0]:
                return "O(n²)"
            else:
                return "O(n)"
        elif loop_count == 1:
            return "O(n)"
        elif "recursi" in code_lower or "return self." in code_lower:
            return "O(log n) to O(n) - recursive"
        else:
            return "O(1)"

    def _estimate_memory_complexity(self, code: str) -> str:
        """Estimate memory complexity"""
        memory_indicators = [
            "[]", "list(", "array", "new int[", "new Array",
            "malloc", "vector", "HashMap", "Dictionary",
            "Set(", "Map("
        ]

        if any(indicator in code for indicator in memory_indicators):
            if "resize" in code or "append" in code or "push" in code:
                return "O(n)"
            else:
                return "O(1) to O(n)"
        else:
            return "O(1)"

    def _generate_suggestions(self, code: str, language: str, metrics: Optional[CodeMetrics]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []

        # Check for missing docstrings/comments
        if language == "python" and '"""' not in code and "def " in code:
            suggestions.append("Add docstrings to functions for better documentation")

        # Check for type hints (Python)
        if language == "python" and "->" not in code and "def " in code:
            suggestions.append("Consider adding type hints for better code clarity")

        # Check for error handling
        error_keywords = ["try", "except", "catch", "throw", "rescue"]
        if not any(kw in code for kw in error_keywords):
            suggestions.append("Consider adding error handling for robustness")

        # Check complexity
        if metrics and metrics.cyclomatic_complexity > 10:
            suggestions.append("Consider refactoring to reduce complexity")

        # Check line length
        lines = code.split('\n')
        if any(len(line) > 100 for line in lines):
            suggestions.append("Some lines exceed 100 characters - consider breaking them up")

        # Check for magic numbers
        import re
        numbers = re.findall(r'\b\d+\b', code)
        if len(numbers) > 5:
            suggestions.append("Consider using named constants instead of magic numbers")

        return suggestions

    def _format_code(self, code: str, language: str) -> str:
        """Format code according to language standards"""
        try:
            if language == "python":
                # Try black first
                try:
                    return black.format_str(code, mode=black.Mode())
                except:
                    # Fallback to autopep8
                    return autopep8.fix_code(code)

            # For other languages, return as-is for now
            # Could integrate prettier for JS/TS, rustfmt for Rust, etc.
            return code

        except Exception as e:
            logger.warning(f"Could not format code: {e}")
            return code