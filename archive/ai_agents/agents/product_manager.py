"""
Product Manager, Marketing Specialist, and Sales/Operations Agents
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


def create_agent_from_persona(persona_name: str) -> ChatAgent:
    """Helper to create agent from persona configuration"""
    if not validate_config():
        raise ValueError("Configuration validation failed. Please set GITHUB_TOKEN.")
    
    persona = getattr(AgentPersonas, persona_name)
    
    openai_client = AsyncOpenAI(
        base_url=GITHUB_BASE_URL,
        api_key=GITHUB_TOKEN,
    )
    
    chat_client = OpenAIChatClient(
        async_client=openai_client,
        model_id=persona["model"]
    )
    
    return ChatAgent(
        chat_client=chat_client,
        name=persona["name"],
        instructions=persona["instructions"]
    )


class ProductManagerAgent:
    """Agent specialized in product management and planning"""
    
    def __init__(self):
        self.agent = create_agent_from_persona("PRODUCT_MANAGER")
    
    async def create_product_roadmap(self, product_description: str) -> AsyncIterator[str]:
        """Create product roadmap"""
        prompt = f"""Create a product roadmap for:

{product_description}

Include:
1. Vision & Goals
2. Quarterly milestones (Q1-Q4)
3. Feature prioritization with RICE scores
4. Success metrics and KPIs
5. Dependencies and risks
6. Resource requirements"""

        thread = self.agent.get_new_thread()
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text


class MarketingSpecialistAgent:
    """Agent specialized in marketing strategy and execution"""
    
    def __init__(self):
        self.agent = create_agent_from_persona("MARKETING_SPECIALIST")
    
    async def create_marketing_strategy(self, business_description: str) -> AsyncIterator[str]:
        """Create comprehensive marketing strategy"""
        prompt = f"""Create a marketing strategy for:

{business_description}

Include:
1. Target audience analysis
2. Brand positioning and messaging
3. Marketing channels and tactics
4. Content marketing calendar (3 months)
5. Social media strategy
6. SEO/SEM approach
7. Budget allocation
8. Metrics and KPIs"""

        thread = self.agent.get_new_thread()
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text


class SalesOperationsAgent:
    """Agent specialized in sales and operations"""
    
    def __init__(self):
        self.agent = create_agent_from_persona("SALES_OPERATIONS")
    
    async def create_sales_process(self, business_description: str) -> AsyncIterator[str]:
        """Create sales process and operations plan"""
        prompt = f"""Create a sales and operations plan for:

{business_description}

Include:
1. Sales funnel design
2. Lead generation strategies
3. Customer outreach templates
4. CRM implementation plan
5. Sales playbook
6. Operations workflows
7. Automation opportunities
8. Performance tracking"""

        thread = self.agent.get_new_thread()
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text
