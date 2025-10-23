"""
@author Tom Butler
@date 2025-10-23
@description LangChain-based code generation service using OpenAI GPT-4.
             Generates code, tests, and documentation based on natural language prompts.
"""
import logging
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
import asyncio
import json

from config import get_settings
from models import GenerationRequest, TestResult, Documentation, CodeMetrics

logger = logging.getLogger(__name__)
settings = get_settings()


class CodeGeneratorService:
    """
    Service for AI-powered code generation.

    Creates separate LLM instance per request using user-provided API key.
    Generates code, unit tests, and documentation for multiple programming languages.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialises code generator with OpenAI API key.

        Args:
            api_key: User's OpenAI API key from Authorization header

        Raises:
            ValueError: If no API key provided
        """
        effective_api_key = api_key or settings.openai_api_key
        if not effective_api_key:
            raise ValueError("OpenAI API key is required")

        self.llm = ChatOpenAI(
            api_key=effective_api_key,
            model=settings.openai_model,
            temperature=settings.openai_temperature,
            max_tokens=settings.openai_max_tokens
        )

    async def generate_code(self, request: GenerationRequest) -> str:
        """
        Generates production-ready code from natural language prompt.

        Args:
            request: Generation request with prompt, language, and options

        Returns:
            Generated code as string

        Raises:
            Exception: If LLM call fails
        """
        try:
            prompt = self._create_code_prompt(request)

            chain = LLMChain(
                llm=self.llm,
                prompt=ChatPromptTemplate.from_template(prompt)
            )

            response = await chain.ainvoke({
                "prompt": request.prompt,
                "language": request.programming_language.value,
                "project_goals": request.project_goals or "General purpose",
                "complexity": request.complexity_level,
                "style_guide": request.style_guide or "Standard conventions"
            })

            code = self._extract_code_from_response(response["text"])
            return code

        except Exception as e:
            logger.error(f"Code generation failed: {str(e)}")
            raise

    async def generate_tests(self, code: str, request: GenerationRequest) -> TestResult:
        """
        Generates unit tests for provided code.

        Selects appropriate test framework based on language.
        Includes edge cases and coverage estimation.

        Args:
            code: Source code to generate tests for
            request: Original generation request for context

        Returns:
            TestResult with test code, framework, and metrics
        """
        try:
            framework = request.test_framework or self._get_default_test_framework(
                request.programming_language.value
            )

            prompt = self._create_test_prompt(code, request, framework)

            chain = LLMChain(
                llm=self.llm,
                prompt=ChatPromptTemplate.from_template(prompt)
            )

            response = await chain.ainvoke({
                "code": code,
                "language": request.programming_language.value,
                "framework": framework
            })

            test_code = self._extract_code_from_response(response["text"])

            return TestResult(
                test_code=test_code,
                framework=framework,
                coverage_estimate=self._estimate_coverage(test_code),
                test_count=self._count_tests(test_code, request.programming_language.value)
            )

        except Exception as e:
            logger.error(f"Test generation failed: {str(e)}")
            raise

    async def generate_documentation(self, code: str, request: GenerationRequest) -> Documentation:
        """
        Generates inline comments, README, and API documentation.

        Args:
            code: Source code to document
            request: Original generation request for context

        Returns:
            Documentation with comments, README, API docs, and examples
        """
        try:
            prompt = self._create_documentation_prompt(code, request)

            chain = LLMChain(
                llm=self.llm,
                prompt=ChatPromptTemplate.from_template(prompt)
            )

            response = await chain.ainvoke({
                "code": code,
                "language": request.programming_language.value,
                "natural_language": request.natural_language.value
            })

            doc_data = self._parse_documentation_response(response["text"])

            return Documentation(
                inline_comments=doc_data.get("inline_comments", code),
                readme=doc_data.get("readme"),
                api_docs=doc_data.get("api_docs"),
                usage_examples=doc_data.get("usage_examples", [])
            )

        except Exception as e:
            logger.error(f"Documentation generation failed: {str(e)}")
            raise

    def _create_code_prompt(self, request: GenerationRequest) -> str:
        return """You are an expert programmer. Generate high-quality, production-ready code based on the following requirements:

User Prompt: {prompt}
Programming Language: {language}
Project Goals: {project_goals}
Complexity Level: {complexity}
Style Guide: {style_guide}

Requirements:
1. Code must be syntactically correct
2. Follow best practices for {language}
3. Include proper error handling
4. Be efficient and optimised
5. Be well-structured and maintainable

Return ONLY the code, wrapped in triple backticks with the language identifier.
Do not include any explanations or comments outside the code block."""

    def _create_test_prompt(self, code: str, request: GenerationRequest, framework: str) -> str:
        return """Generate comprehensive unit tests for the following code:

Code to test:
```{language}
{code}
```

Test Framework: {framework}
Language: {language}

Requirements:
1. Cover all functions/methods
2. Include edge cases
3. Test error conditions
4. Follow {framework} best practices
5. Aim for high code coverage

Return ONLY the test code, wrapped in triple backticks with the language identifier."""

    def _create_documentation_prompt(self, code: str, request: GenerationRequest) -> str:
        return """Generate comprehensive documentation for the following code:

Code to document:
```{language}
{code}
```

Natural Language: {natural_language}

Please provide:
1. Code with inline comments explaining complex logic
2. A README section describing what the code does
3. API documentation if applicable
4. 2-3 usage examples

Format your response as JSON with the following structure:
{{
    "inline_comments": "code with comments",
    "readme": "README content",
    "api_docs": "API documentation or null",
    "usage_examples": ["example1", "example2"]
}}"""

    def _extract_code_from_response(self, response: str) -> str:
        """Extract code from LLM response"""
        import re

        # Try to find code block with language identifier
        pattern = r"```[\w]*\n(.*?)\n```"
        match = re.search(pattern, response, re.DOTALL)

        if match:
            return match.group(1).strip()

        # Try to find code block without language identifier
        pattern = r"```(.*?)```"
        match = re.search(pattern, response, re.DOTALL)

        if match:
            return match.group(1).strip()

        # Return the whole response if no code block found
        return response.strip()

    def _parse_documentation_response(self, response: str) -> Dict[str, Any]:
        """Parse documentation response from LLM"""
        try:
            # Try to parse as JSON
            import re
            json_pattern = r'\{.*\}'
            match = re.search(json_pattern, response, re.DOTALL)

            if match:
                return json.loads(match.group(0))
        except:
            pass

        # Fallback: create basic structure
        return {
            "inline_comments": response,
            "readme": None,
            "api_docs": None,
            "usage_examples": []
        }

    def _get_default_test_framework(self, language: str) -> str:
        """Get default test framework for a language"""
        frameworks = {
            "python": "pytest",
            "javascript": "jest",
            "typescript": "jest",
            "java": "junit",
            "csharp": "xunit",
            "go": "testing",
            "rust": "cargo test",
            "cpp": "gtest",
            "ruby": "rspec",
            "swift": "xctest"
        }
        return frameworks.get(language, "unittest")

    def _estimate_coverage(self, test_code: str) -> float:
        """Estimate test coverage based on test code"""
        # Simple heuristic based on test count and assertions
        test_indicators = ["test_", "Test", "assert", "expect", "should", "describe", "it("]
        count = sum(1 for indicator in test_indicators if indicator in test_code)

        if count >= 10:
            return 85.0
        elif count >= 5:
            return 70.0
        elif count >= 2:
            return 50.0
        else:
            return 30.0

    def _count_tests(self, test_code: str, language: str) -> int:
        """Count number of test cases"""
        patterns = {
            "python": r"def test_|class Test",
            "javascript": r"test\(|it\(|describe\(",
            "typescript": r"test\(|it\(|describe\(",
            "java": r"@Test|void test",
            "csharp": r"\[Test\]|\[Fact\]",
            "go": r"func Test",
            "rust": r"#\[test\]",
            "cpp": r"TEST\(|TEST_F\(",
            "ruby": r"it |describe |context ",
            "swift": r"func test"
        }

        import re
        pattern = patterns.get(language, r"test")
        matches = re.findall(pattern, test_code, re.IGNORECASE)
        return len(matches) if matches else 1

    async def calculate_metrics(self, code: str, language: str) -> CodeMetrics:
        """Calculate code quality metrics"""
        lines = code.split('\n')
        loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])

        # Simple cyclomatic complexity estimation
        complexity_indicators = ['if ', 'elif ', 'else:', 'for ', 'while ', 'except:', 'case ']
        complexity = sum(1 for line in lines for indicator in complexity_indicators if indicator in line) + 1

        # Readability score (simple heuristic)
        avg_line_length = sum(len(line) for line in lines) / max(len(lines), 1)
        readability = max(0, min(100, 100 - (avg_line_length - 50) * 2))

        return CodeMetrics(
            lines_of_code=loc,
            cyclomatic_complexity=complexity,
            readability_score=round(readability, 1),
            estimated_execution_time=self._estimate_complexity(code),
            memory_complexity=self._estimate_memory_complexity(code)
        )

    def _estimate_complexity(self, code: str) -> str:
        """Estimate time complexity"""
        if "for" in code and "for" in code[code.index("for")+4:]:
            return "O(n²)"
        elif "for" in code or "while" in code:
            return "O(n)"
        else:
            return "O(1)"

    def _estimate_memory_complexity(self, code: str) -> str:
        """Estimate memory complexity"""
        if "[]" in code or "list(" in code or "array" in code.lower():
            return "O(n)"
        else:
            return "O(1)"