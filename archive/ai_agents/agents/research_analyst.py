"""
Research Analyst Agent - Comprehensive Research and Analysis
"""

import sys
import os
from typing import AsyncIterator
from datetime import datetime

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


class ResearchAnalystAgent:
    """Agent specialized in research, analysis, and documentation"""
    
    def __init__(self):
        """Initialize the Research Analyst Agent"""
        if not validate_config():
            raise ValueError("Configuration validation failed. Please set GITHUB_TOKEN.")
        
        self.openai_client = AsyncOpenAI(
            base_url=GITHUB_BASE_URL,
            api_key=GITHUB_TOKEN,
        )
        
        persona = AgentPersonas.RESEARCH_ANALYST
        
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
        """Define tools available to the Research Analyst"""
        from typing import Annotated
        
        def search_topic(
            query: Annotated[str, "Search query or research topic"],
            focus_area: Annotated[str, "Specific focus area (e.g., 'academic', 'industry', 'trends', 'statistics')"]
        ) -> str:
            """Search for information on a topic"""
            # Placeholder - in production, integrate with web search APIs
            return f"""Research Results for: "{query}"
Focus Area: {focus_area}

[Note: This is a simulation. In production, integrate with:]
- Google Scholar API for academic research
- News APIs for industry trends
- Statistical databases for data
- Industry reports (Gartner, Forrester, etc.)

Key Areas to Explore:
1. Current state and recent developments
2. Key players and stakeholders
3. Market trends and projections
4. Challenges and opportunities
5. Expert opinions and analysis

Recommendation: Cross-reference multiple sources for accuracy."""
        
        def analyze_trends(
            data_description: Annotated[str, "Description of data or trend to analyze"],
            time_period: Annotated[str, "Time period for analysis (e.g., '2020-2025', 'last 5 years')"]
        ) -> str:
            """Analyze trends in data or market"""
            return f"""Trend Analysis: {data_description}
Time Period: {time_period}

Analysis Framework:

1. Historical Context:
   - Previous trends and patterns
   - Key inflection points
   - Cyclical patterns

2. Current State:
   - Present situation
   - Recent changes
   - Driving factors

3. Future Projections:
   - Likely trajectory
   - Growth estimates
   - Potential disruptions

4. Implications:
   - Strategic considerations
   - Opportunities
   - Threats

Methods Used:
- Time series analysis
- Comparative analysis
- Pattern recognition
- Expert synthesis

Confidence Level: [Based on data availability and quality]"""
        
        def create_research_summary(
            topic: Annotated[str, "Research topic"],
            key_points: Annotated[str, "Main findings (comma or newline separated)"]
        ) -> str:
            """Create a structured research summary"""
            return f"""RESEARCH SUMMARY
{datetime.now().strftime('%Y-%m-%d')}

Topic: {topic}

EXECUTIVE SUMMARY:
[High-level overview of findings]

KEY FINDINGS:
{key_points}

METHODOLOGY:
- Literature review
- Data analysis
- Expert consultation
- Comparative analysis

CONCLUSIONS:
[Main takeaways]

RECOMMENDATIONS:
[Actionable insights]

SOURCES & CITATIONS:
[List of references]

NEXT STEPS:
[Further research areas]"""
        
        return [
            search_topic,
            analyze_trends,
            create_research_summary
        ]
    
    async def research_topic(
        self, 
        topic: str, 
        depth: str = "comprehensive",
        specific_questions: str = ""
    ) -> AsyncIterator[str]:
        """
        Conduct research on a topic
        
        Args:
            topic: Research topic or question
            depth: Level of depth ('quick', 'moderate', 'comprehensive')
            specific_questions: Specific questions to answer
        
        Yields:
            Streamed response chunks
        """
        prompt = f"""Conduct {depth} research on the following topic:

Topic: {topic}

{f'Specific Questions to Answer:{specific_questions}' if specific_questions else ''}

Provide a well-structured research report including:

1. EXECUTIVE SUMMARY
   - Overview of key findings
   - Main conclusions

2. BACKGROUND & CONTEXT
   - Current state
   - Historical perspective
   - Why this matters

3. KEY FINDINGS
   - Main discoveries
   - Important data points
   - Trends and patterns

4. DETAILED ANALYSIS
   - In-depth examination
   - Multiple perspectives
   - Supporting evidence

5. TRENDS & IMPLICATIONS
   - Current trends
   - Future projections
   - Strategic implications

6. RECOMMENDATIONS
   - Actionable insights
   - Next steps
   - Further research areas

7. SOURCES & METHODOLOGY
   - Research approach
   - Key sources
   - Data quality notes

Be thorough, objective, and cite sources where appropriate."""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text
    
    async def competitive_research(
        self, 
        company_or_product: str,
        competitors: str
    ) -> AsyncIterator[str]:
        """Conduct competitive research and analysis"""
        prompt = f"""Conduct competitive research on:

Primary Subject: {company_or_product}
Competitors: {competitors}

Provide comprehensive competitive analysis:

1. MARKET OVERVIEW
   - Market size and growth
   - Key segments
   - Market dynamics

2. COMPETITOR PROFILES
   For each competitor:
   - Company overview
   - Products/services
   - Market position
   - Strengths/weaknesses
   - Recent developments

3. FEATURE COMPARISON
   - Feature matrix
   - Unique differentiators
   - Technology stack
   - Pricing models

4. MARKET POSITIONING
   - Target audiences
   - Brand perception
   - Marketing strategies
   - Value propositions

5. SWOT ANALYSIS
   For primary subject vs competitors

6. OPPORTUNITIES & GAPS
   - Market gaps
   - Underserved needs
   - Differentiation opportunities

7. STRATEGIC RECOMMENDATIONS
   - Competitive strategy
   - Positioning advice
   - Priority actions"""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text
    
    async def trend_analysis(
        self, 
        industry: str,
        time_horizon: str = "5 years"
    ) -> AsyncIterator[str]:
        """Analyze industry trends and future projections"""
        prompt = f"""Analyze trends in the {industry} industry:

Time Horizon: {time_horizon}

Provide comprehensive trend analysis:

1. CURRENT STATE
   - Industry overview
   - Key metrics
   - Major players

2. HISTORICAL TRENDS (Past 5 Years)
   - Major changes
   - Growth patterns
   - Key milestones

3. EMERGING TRENDS
   - New technologies
   - Changing consumer behavior
   - Regulatory changes
   - Market shifts

4. DRIVERS & CATALYSTS
   - What's driving change
   - Key influencers
   - External factors

5. FUTURE PROJECTIONS
   - Expected developments
   - Growth forecasts
   - Potential disruptions

6. OPPORTUNITIES & THREATS
   - Opportunities to capitalize on
   - Risks to mitigate

7. STRATEGIC IMPLICATIONS
   - What this means for businesses
   - Recommended actions
   - Positioning strategies"""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text


# CLI Interface
async def main():
    """Command-line interface for Research Analyst Agent"""
    import asyncio
    
    print("🔬 Research Analyst Agent")
    print("=" * 50)
    
    agent = ResearchAnalystAgent()
    
    print("\nWhat type of research would you like?")
    print("1. General topic research")
    print("2. Competitive research")
    print("3. Industry trend analysis")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n📝 Enter research topic:")
        topic = input("> ").strip()
        
        print("\n📝 Research depth (quick/moderate/comprehensive):")
        depth = input("> ").strip() or "comprehensive"
        
        print("\n📝 Specific questions (optional):")
        questions = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Research Report:\n")
        
        async for chunk in agent.research_topic(topic, depth, questions):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "2":
        print("\n📝 Company or product to research:")
        subject = input("> ").strip()
        
        print("\n📝 Competitors (comma-separated):")
        competitors = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Competitive Analysis:\n")
        
        async for chunk in agent.competitive_research(subject, competitors):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "3":
        print("\n📝 Industry to analyze:")
        industry = input("> ").strip()
        
        print("\n📝 Time horizon (e.g., '5 years', '2025-2030'):")
        horizon = input("> ").strip() or "5 years"
        
        print("\n" + "=" * 50)
        print("🤖 Trend Analysis:\n")
        
        async for chunk in agent.trend_analysis(industry, horizon):
            print(chunk, end="", flush=True)
        print("\n")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
