"""
Orchestrator Agent - Coordinates Multiple Specialist Agents
"""

import sys
import os
from typing import AsyncIterator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import GroupChatBuilder, ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI
from config import (
    GITHUB_TOKEN,
    GITHUB_BASE_URL,
    AgentPersonas,
    validate_config
)

from .business_strategist import BusinessStrategistAgent
from .research_analyst import ResearchAnalystAgent
from .code_engineer import CodeEngineerAgent
from .product_manager import ProductManagerAgent, MarketingSpecialistAgent, SalesOperationsAgent


class OrchestratorAgent:
    """
    Orchestrator that coordinates multiple specialist agents
    Uses GroupChat pattern for multi-agent workflows
    """
    
    def __init__(self):
        """Initialize orchestrator with all specialist agents"""
        if not validate_config():
            raise ValueError("Configuration validation failed. Please set GITHUB_TOKEN.")
        
        # Initialize OpenAI client for the manager
        self.openai_client = AsyncOpenAI(
            base_url=GITHUB_BASE_URL,
            api_key=GITHUB_TOKEN,
        )
        
        # Create specialist agents
        self.business_strategist = BusinessStrategistAgent().agent
        self.research_analyst = ResearchAnalystAgent().agent
        self.code_engineer = CodeEngineerAgent().agent
        self.product_manager = ProductManagerAgent().agent
        self.marketing_specialist = MarketingSpecialistAgent().agent
        self.sales_operations = SalesOperationsAgent().agent
        
        # Create manager agent for orchestration
        persona = AgentPersonas.ORCHESTRATOR
        chat_client = OpenAIChatClient(
            async_client=self.openai_client,
            model_id=persona["model"]
        )
        
        self.manager = ChatAgent(
            chat_client=chat_client,
            name=persona["name"],
            instructions=persona["instructions"]
        )
    
    def create_workflow_for_task(self, task_type: str = "full_business"):
        """
        Create a workflow based on task type
        
        Args:
            task_type: Type of workflow
                - "business_evaluation": Business idea evaluation
                - "research": Research and analysis
                - "coding": Code development
                - "full_business": Complete business setup (all agents)
        """
        participants = []
        
        if task_type == "business_evaluation":
            participants = [
                self.business_strategist,
                self.research_analyst
            ]
        elif task_type == "research":
            participants = [self.research_analyst]
        elif task_type == "coding":
            participants = [self.code_engineer]
        elif task_type == "full_business":
            participants = [
                self.business_strategist,
                self.research_analyst,
                self.product_manager,
                self.marketing_specialist,
                self.sales_operations,
                self.code_engineer
            ]
        else:
            raise ValueError(f"Unknown task_type: {task_type}")
        
        # Build group chat workflow
        workflow = (
            GroupChatBuilder()
            .set_manager(self.manager, display_name="Orchestrator")
            .participants(participants)
            .with_max_rounds(20)  # Limit to prevent infinite loops
            .build()
        )
        
        return workflow
    
    async def run_business_evaluation(
        self, 
        idea: str,
        context: str = ""
    ) -> AsyncIterator[str]:
        """
        Evaluate a business idea using Business Strategist and Research Analyst
        
        Args:
            idea: Business idea description
            context: Additional context
        
        Yields:
            Streamed responses from agents
        """
        workflow = self.create_workflow_for_task("business_evaluation")
        
        task = f"""Evaluate this business idea for market viability:

Business Idea: {idea}
Context: {context if context else "None"}

Collaboration Plan:
1. Research Analyst: Conduct market research and competitive analysis
2. Business Strategist: Evaluate viability and create action plan
3. Provide comprehensive evaluation with next steps"""

        async for event in workflow.run_stream(task):
            if hasattr(event, 'text') and event.text:
                yield event.text
    
    async def run_complete_business_setup(
        self, 
        business_idea: str,
        duration_weeks: int = 12
    ) -> AsyncIterator[str]:
        """
        Complete solopreneur business setup using all agents
        
        Args:
            business_idea: Description of the business
            duration_weeks: Timeline for setup
        
        Yields:
            Streamed responses from agents
        """
        workflow = self.create_workflow_for_task("full_business")
        
        task = f"""Help me launch a complete solopreneur business:

Business Idea: {business_idea}
Timeline: {duration_weeks} weeks

Requirements:
1. Business Strategy: Market analysis, viability assessment, go-to-market plan
2. Research: Competitive analysis, industry trends, customer insights
3. Product Planning: Roadmap, features, MVP definition
4. Marketing: Brand positioning, content strategy, customer acquisition
5. Sales & Operations: Sales process, CRM setup, operations workflows
6. Technology: Tech stack recommendations, development plan, automation

Coordinate all agents to deliver a comprehensive business launch plan."""

        async for event in workflow.run_stream(task):
            if hasattr(event, 'text') and event.text:
                yield event.text
    
    async def run_research_project(
        self, 
        research_topic: str,
        depth: str = "comprehensive"
    ) -> AsyncIterator[str]:
        """
        Conduct research using Research Analyst
        
        Args:
            research_topic: Topic to research
            depth: Research depth
        
        Yields:
            Streamed responses
        """
        workflow = self.create_workflow_for_task("research")
        
        task = f"""Conduct {depth} research on:

Topic: {research_topic}

Provide a comprehensive research report with:
- Executive summary
- Key findings
- Analysis and insights
- Recommendations
- Sources and methodology"""

        async for event in workflow.run_stream(task):
            if hasattr(event, 'text') and event.text:
                yield event.text
    
    async def run_coding_project(
        self, 
        project_description: str,
        requirements: str = ""
    ) -> AsyncIterator[str]:
        """
        Execute coding project using Code Engineer
        
        Args:
            project_description: What to build
            requirements: Additional requirements
        
        Yields:
            Streamed responses
        """
        workflow = self.create_workflow_for_task("coding")
        
        task = f"""Develop the following:

Project: {project_description}
Requirements: {requirements if requirements else "None specified"}

Provide:
- Complete code
- Setup instructions
- Testing strategy
- Deployment guide"""

        async for event in workflow.run_stream(task):
            if hasattr(event, 'text') and event.text:
                yield event.text


# CLI Interface
async def main():
    """Command-line interface for Orchestrator"""
    import asyncio
    
    print("🎯 AI Agent Orchestrator")
    print("=" * 50)
    
    orchestrator = OrchestratorAgent()
    
    print("\nWhat would you like to do?")
    print("1. Evaluate a business idea")
    print("2. Complete business setup (solopreneur)")
    print("3. Research a topic")
    print("4. Coding project")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n📝 Enter your business idea:")
        idea = input("> ").strip()
        print("\n📝 Additional context (optional):")
        context = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Multi-Agent Evaluation:\n")
        
        async for chunk in orchestrator.run_business_evaluation(idea, context):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "2":
        print("\n📝 Describe your business:")
        idea = input("> ").strip()
        print("\n📝 Timeline in weeks (default 12):")
        weeks_input = input("> ").strip()
        weeks = int(weeks_input) if weeks_input else 12
        
        print("\n" + "=" * 50)
        print("🤖 Complete Business Setup:\n")
        
        async for chunk in orchestrator.run_complete_business_setup(idea, weeks):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "3":
        print("\n📝 Research topic:")
        topic = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Research Report:\n")
        
        async for chunk in orchestrator.run_research_project(topic):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "4":
        print("\n📝 Describe what you want to build:")
        project = input("> ").strip()
        print("\n📝 Additional requirements (optional):")
        requirements = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Code Generation:\n")
        
        async for chunk in orchestrator.run_coding_project(project, requirements):
            print(chunk, end="", flush=True)
        print("\n")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
