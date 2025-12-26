"""
Code Engineer Agent - Software Development and Automation
"""

import sys
import os
from typing import AsyncIterator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI
from config import (
    GITHUB_TOKEN,
    GITHUB_BASE_URL,
    AgentPersonas,
    validate_config
)


class CodeEngineerAgent:
    """Agent specialized in software development and automation"""
    
    def __init__(self):
        """Initialize the Code Engineer Agent"""
        if not validate_config():
            raise ValueError("Configuration validation failed. Please set GITHUB_TOKEN.")
        
        self.openai_client = AsyncOpenAI(
            base_url=GITHUB_BASE_URL,
            api_key=GITHUB_TOKEN,
        )
        
        persona = AgentPersonas.CODE_ENGINEER
        
        self.chat_client = OpenAIChatClient(
            async_client=self.openai_client,
            model_id=persona["model"]
        )
        
        self.agent = ChatAgent(
            chat_client=self.chat_client,
            name=persona["name"],
            instructions=persona["instructions"],
            tools=self._get_tools()
        )
    
    def _get_tools(self) -> list:
        """Define tools available to the Code Engineer"""
        from typing import Annotated
        
        def generate_file_structure(
            project_type: Annotated[str, "Type of project (e.g., 'flask-api', 'react-app', 'data-pipeline')"],
            features: Annotated[str, "Key features (comma-separated)"]
        ) -> str:
            """Generate project folder structure"""
            
            structures = {
                "flask-api": """
project_name/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── tests/
├── config.py
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md""",
                
                "react-app": """
project_name/
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── utils/
│   ├── styles/
│   ├── App.jsx
│   └── index.jsx
├── package.json
├── .env.example
└── README.md""",
                
                "data-pipeline": """
project_name/
├── pipelines/
│   ├── extract/
│   ├── transform/
│   └── load/
├── models/
├── utils/
├── tests/
├── config/
├── requirements.txt
└── README.md"""
            }
            
            base_structure = structures.get(project_type, "Standard project structure")
            
            return f"""Project Structure for {project_type}:
Features: {features}

{base_structure}

Recommended files based on features:
- Add 'auth/' for authentication features
- Add 'middleware/' for custom middleware
- Add 'migrations/' for database migrations
- Add 'docs/' for API documentation
- Add 'scripts/' for utility scripts
"""
        
        def suggest_tech_stack(
            project_description: Annotated[str, "Description of the project"],
            constraints: Annotated[str, "Any constraints (e.g., 'must use Python', 'serverless', 'low-cost')"]
        ) -> str:
            """Suggest appropriate technology stack"""
            return f"""Technology Stack Recommendations

Project: {project_description}
Constraints: {constraints}

RECOMMENDED STACK:

Backend:
- Language: [Python/Node.js/etc]
- Framework: [FastAPI/Express/Django/etc]
- Database: [PostgreSQL/MongoDB/etc]
- Caching: [Redis/Memcached]
- Queue: [Celery/RabbitMQ/SQS]

Frontend (if applicable):
- Framework: [React/Vue/Next.js]
- State Management: [Redux/Context/Zustand]
- Styling: [Tailwind/Material-UI]

Infrastructure:
- Hosting: [AWS/Azure/Vercel/Railway]
- CI/CD: [GitHub Actions/GitLab CI]
- Monitoring: [Datadog/New Relic/Sentry]
- Logging: [CloudWatch/Elasticsearch]

Development Tools:
- Version Control: Git
- Package Manager: [npm/pip/poetry]
- Testing: [pytest/jest/etc]
- Linting: [eslint/flake8]

Rationale: [Why these choices]

Alternatives: [Other options to consider]
"""
        
        def create_deployment_script(
            platform: Annotated[str, "Deployment platform (e.g., 'docker', 'aws', 'heroku')"],
            app_type: Annotated[str, "Application type (e.g., 'web-api', 'background-worker')"]
        ) -> str:
            """Generate deployment configuration"""
            
            if platform.lower() == "docker":
                return """# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - .:/app
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
            
            return f"Deployment configuration for {platform} - {app_type}"
        
        def review_code_snippet(
            code: Annotated[str, "Code snippet to review"],
            language: Annotated[str, "Programming language"]
        ) -> str:
            """Review code and suggest improvements"""
            return f"""Code Review - {language}

Code:
{code}

ANALYSIS:

1. Correctness: ✓/✗
   [Issues with logic or bugs]

2. Performance: ✓/⚠/✗
   [Performance concerns]

3. Security: ✓/⚠/✗
   [Security vulnerabilities]

4. Best Practices: ✓/⚠/✗
   [Code style, patterns]

5. Maintainability: ✓/⚠/✗
   [Readability, documentation]

RECOMMENDATIONS:
- [Specific improvements]
- [Alternative approaches]
- [Best practice suggestions]

REFACTORED CODE:
[Improved version]
"""
        
        return [
            generate_file_structure,
            suggest_tech_stack,
            create_deployment_script,
            review_code_snippet
        ]
    
    async def generate_code(
        self, 
        task: str,
        language: str = "python",
        framework: str = "",
        requirements: str = ""
    ) -> AsyncIterator[str]:
        """
        Generate code for a specific task
        
        Args:
            task: Description of what the code should do
            language: Programming language
            framework: Framework to use (if any)
            requirements: Additional requirements
        
        Yields:
            Streamed response chunks
        """
        prompt = f"""Generate production-ready code for the following task:

Task: {task}
Language: {language}
{f'Framework: {framework}' if framework else ''}
{f'Requirements: {requirements}' if requirements else ''}

Provide:

1. COMPLETE CODE
   - All necessary files
   - Proper structure
   - Error handling
   - Input validation

2. CODE EXPLANATION
   - How it works
   - Key decisions
   - Design patterns used

3. DEPENDENCIES
   - Required packages
   - Installation commands

4. USAGE INSTRUCTIONS
   - How to run
   - Configuration needed
   - Example usage

5. TESTING
   - Test cases
   - How to test
   - Expected output

6. DEPLOYMENT NOTES
   - Environment setup
   - Security considerations
   - Performance tips

Make the code:
- Production-ready
- Well-documented
- Following best practices
- Secure and efficient
- Easy to maintain"""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text
    
    async def debug_code(
        self, 
        code: str,
        error_message: str,
        context: str = ""
    ) -> AsyncIterator[str]:
        """Debug code and fix issues"""
        prompt = f"""Help debug this code:

CODE:
{code}

ERROR MESSAGE:
{error_message}

{f'ADDITIONAL CONTEXT:{context}' if context else ''}

Please:
1. Identify the root cause of the error
2. Explain why the error occurs
3. Provide the fixed code
4. Suggest how to prevent similar issues
5. Recommend testing strategies"""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text
    
    async def create_automation_script(
        self, 
        automation_goal: str,
        target_system: str = "local",
        frequency: str = ""
    ) -> AsyncIterator[str]:
        """Create automation scripts"""
        prompt = f"""Create an automation script for:

Goal: {automation_goal}
Target System: {target_system} (local/remote/cloud)
{f'Frequency: {frequency}' if frequency else ''}

Provide:

1. AUTOMATION SCRIPT
   - Complete, working code
   - Error handling
   - Logging
   - Retry logic

2. SETUP INSTRUCTIONS
   - Prerequisites
   - Configuration
   - Credentials management

3. SCHEDULING
   - How to schedule (cron/Task Scheduler/cloud)
   - Recommended frequency
   - Monitoring setup

4. ERROR HANDLING
   - What can go wrong
   - How to handle failures
   - Alerting strategy

5. TESTING
   - How to test safely
   - Dry-run mode
   - Validation checks

Make it robust, secure, and production-ready."""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text
    
    async def setup_ci_cd(
        self, 
        project_description: str,
        deployment_target: str,
        test_framework: str = ""
    ) -> AsyncIterator[str]:
        """Create CI/CD pipeline configuration"""
        prompt = f"""Create a CI/CD pipeline for:

Project: {project_description}
Deployment Target: {deployment_target}
{f'Test Framework: {test_framework}' if test_framework else ''}

Provide:

1. CI/CD CONFIGURATION
   - Complete workflow file (GitHub Actions/GitLab CI/etc.)
   - Build steps
   - Test steps
   - Deploy steps

2. ENVIRONMENT SETUP
   - Required secrets
   - Environment variables
   - Service connections

3. TESTING STRATEGY
   - Unit tests
   - Integration tests
   - E2E tests
   - Coverage requirements

4. DEPLOYMENT STRATEGY
   - Blue-green/Rolling/Canary
   - Health checks
   - Rollback procedure

5. MONITORING & ALERTS
   - What to monitor
   - Alert thresholds
   - Notification channels

Make it production-grade with proper safeguards."""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text


# CLI Interface
async def main():
    """Command-line interface for Code Engineer Agent"""
    import asyncio
    
    print("💻 Code Engineer Agent")
    print("=" * 50)
    
    agent = CodeEngineerAgent()
    
    print("\nWhat would you like to do?")
    print("1. Generate code")
    print("2. Debug code")
    print("3. Create automation script")
    print("4. Setup CI/CD pipeline")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n📝 Describe what the code should do:")
        task = input("> ").strip()
        
        print("\n📝 Programming language (default: python):")
        language = input("> ").strip() or "python"
        
        print("\n📝 Framework (optional):")
        framework = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Generated Code:\n")
        
        async for chunk in agent.generate_code(task, language, framework):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "2":
        print("\n📝 Paste your code:")
        print("(Type 'END' on a new line when done)")
        code_lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            code_lines.append(line)
        code = "\n".join(code_lines)
        
        print("\n📝 Error message:")
        error = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Debug Analysis:\n")
        
        async for chunk in agent.debug_code(code, error):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "3":
        print("\n📝 What should the automation do:")
        goal = input("> ").strip()
        
        print("\n📝 Target system (local/remote/cloud):")
        target = input("> ").strip() or "local"
        
        print("\n" + "=" * 50)
        print("🤖 Automation Script:\n")
        
        async for chunk in agent.create_automation_script(goal, target):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "4":
        print("\n📝 Describe your project:")
        project = input("> ").strip()
        
        print("\n📝 Deployment target (e.g., AWS, Vercel, Docker):")
        target = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 CI/CD Configuration:\n")
        
        async for chunk in agent.setup_ci_cd(project, target):
            print(chunk, end="", flush=True)
        print("\n")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
