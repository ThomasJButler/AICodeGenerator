"""Test fixtures and mock data for integration tests."""
from typing import Dict, Any


class MockResponses:
    """Collection of mock responses for testing."""

    @staticmethod
    def python_hello_world() -> str:
        """Python hello world function."""
        return """def hello_world():
    '''A simple hello world function.'''
    return "Hello, World!"
"""

    @staticmethod
    def javascript_hello_world() -> str:
        """JavaScript hello world function."""
        return """function helloWorld() {
    // A simple hello world function
    return "Hello, World!";
}
"""

    @staticmethod
    def python_fibonacci() -> str:
        """Python fibonacci function."""
        return """def fibonacci(n):
    '''Calculate fibonacci number at position n.'''
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""

    @staticmethod
    def python_test_hello_world() -> str:
        """Python test for hello world."""
        return """import unittest
from main import hello_world

class TestHelloWorld(unittest.TestCase):
    def test_hello_world_returns_string(self):
        '''Test that hello_world returns a string.'''
        result = hello_world()
        self.assertIsInstance(result, str)

    def test_hello_world_returns_correct_message(self):
        '''Test that hello_world returns the correct message.'''
        result = hello_world()
        self.assertEqual(result, "Hello, World!")

if __name__ == '__main__':
    unittest.main()
"""

    @staticmethod
    def javascript_test_hello_world() -> str:
        """JavaScript test for hello world."""
        return """describe('helloWorld', () => {
    test('returns a string', () => {
        const result = helloWorld();
        expect(typeof result).toBe('string');
    });

    test('returns correct message', () => {
        const result = helloWorld();
        expect(result).toBe('Hello, World!');
    });
});
"""

    @staticmethod
    def documentation_hello_world() -> str:
        """Documentation for hello world function."""
        return """# Hello World Function

## Description
A simple function that returns a greeting message. This function demonstrates
the basic syntax and structure of a function in the chosen programming language.

## Usage

### Python
```python
from main import hello_world

message = hello_world()
print(message)  # Output: Hello, World!
```

### JavaScript
```javascript
const message = helloWorld();
console.log(message);  // Output: Hello, World!
```

## Parameters
None

## Returns
- **string**: A greeting message "Hello, World!"

## Examples
```python
>>> hello_world()
'Hello, World!'
```

## Notes
- This is a basic function with no parameters
- Always returns the same string value
- Useful for testing basic functionality
"""


class TestData:
    """Test data for various scenarios."""

    @staticmethod
    def complex_python_code() -> str:
        """Complex Python code for testing analysis."""
        return """
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True

class UserService:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self._next_id = 1

    async def create_user(self, name: str, email: str) -> User:
        '''Create a new user.'''
        user = User(
            id=self._next_id,
            name=name,
            email=email
        )
        self.users[user.id] = user
        self._next_id += 1
        await self._send_welcome_email(user)
        return user

    async def get_user(self, user_id: int) -> Optional[User]:
        '''Get user by ID.'''
        return self.users.get(user_id)

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        '''Update user attributes.'''
        user = self.users.get(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
        return user

    async def delete_user(self, user_id: int) -> bool:
        '''Delete a user.'''
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    async def get_active_users(self) -> List[User]:
        '''Get all active users.'''
        return [u for u in self.users.values() if u.active]

    async def _send_welcome_email(self, user: User) -> None:
        '''Send welcome email to new user.'''
        await asyncio.sleep(0.1)  # Simulate email sending
        print(f"Welcome email sent to {user.email}")
"""

    @staticmethod
    def invalid_python_code() -> str:
        """Invalid Python code for error testing."""
        return """
def broken_function(:  # Missing parameter name
    print("This won't work"
    return None  # Missing closing parenthesis above

class IncompleteClas  # Missing colon
    def __init__(self)
        self.value = 10  # Missing colon above
"""

    @staticmethod
    def various_languages_samples() -> Dict[str, str]:
        """Sample code in various languages."""
        return {
            "python": "def greet(name):\n    return f'Hello, {name}!'",
            "javascript": "const greet = (name) => `Hello, ${name}!`;",
            "typescript": "const greet = (name: string): string => `Hello, ${name}!`;",
            "java": "public String greet(String name) {\n    return \"Hello, \" + name + \"!\";\n}",
            "csharp": "public string Greet(string name) => $\"Hello, {name}!\";",
            "go": "func greet(name string) string {\n    return fmt.Sprintf(\"Hello, %s!\", name)\n}",
            "rust": "fn greet(name: &str) -> String {\n    format!(\"Hello, {}!\", name)\n}",
            "cpp": "std::string greet(const std::string& name) {\n    return \"Hello, \" + name + \"!\";\n}",
            "ruby": "def greet(name)\n  \"Hello, #{name}!\"\nend",
            "swift": "func greet(_ name: String) -> String {\n    return \"Hello, \\(name)!\"\n}"
        }


class APIResponses:
    """Mock API response structures."""

    @staticmethod
    def generation_response(
        code: str = None,
        tests: str = None,
        documentation: str = None,
        language: str = "python"
    ) -> Dict[str, Any]:
        """Create a mock generation API response."""
        return {
            "id": "gen_12345",
            "code": code or MockResponses.python_hello_world(),
            "tests": tests,
            "documentation": documentation,
            "language": language,
            "metrics": {
                "lines_of_code": 3,
                "cyclomatic_complexity": 1,
                "readability_score": 95
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }

    @staticmethod
    def analysis_response(
        syntax_valid: bool = True,
        complexity: int = 1
    ) -> Dict[str, Any]:
        """Create a mock analysis API response."""
        return {
            "syntax_valid": syntax_valid,
            "complexity": complexity,
            "lines_of_code": 10,
            "readability_score": 85,
            "performance_score": 75,
            "suggestions": [
                "Consider adding type hints",
                "Add error handling"
            ],
            "syntax_errors": [] if syntax_valid else ["Syntax error on line 2"]
        }

    @staticmethod
    def languages_response() -> Dict[str, Any]:
        """Create a mock languages API response."""
        return {
            "languages": [
                {"value": "cpp", "label": "C++", "extension": ".cpp", "test_framework": "Google Test"},
                {"value": "csharp", "label": "C#", "extension": ".cs", "test_framework": "NUnit"},
                {"value": "go", "label": "Go", "extension": ".go", "test_framework": "testing"},
                {"value": "java", "label": "Java", "extension": ".java", "test_framework": "JUnit"},
                {"value": "javascript", "label": "JavaScript", "extension": ".js", "test_framework": "Jest"},
                {"value": "python", "label": "Python", "extension": ".py", "test_framework": "pytest"},
                {"value": "ruby", "label": "Ruby", "extension": ".rb", "test_framework": "RSpec"},
                {"value": "rust", "label": "Rust", "extension": ".rs", "test_framework": "cargo test"},
                {"value": "swift", "label": "Swift", "extension": ".swift", "test_framework": "XCTest"},
                {"value": "typescript", "label": "TypeScript", "extension": ".ts", "test_framework": "Jest"}
            ]
        }