"""
Business Strategist Agent - Market Analysis and Business Evaluation
"""

import sys
import os
from typing import Any, AsyncIterator

# Add parent directory to path for imports
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


class BusinessStrategistAgent:
    """Agent specialized in business strategy and market evaluation"""
    
    def __init__(self):
        """Initialize the Business Strategist Agent"""
        if not validate_config():
            raise ValueError("Configuration validation failed. Please set GITHUB_TOKEN.")
        
        self.openai_client = AsyncOpenAI(
            base_url=GITHUB_BASE_URL,
            api_key=GITHUB_TOKEN,
        )
        
        persona = AgentPersonas.BUSINESS_STRATEGIST
        
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
        """Define tools available to the Business Strategist"""
        from typing import Annotated
        
        def calculate_market_size(
            target_audience: Annotated[str, "Description of target audience"],
            geography: Annotated[str, "Geographic market (e.g., 'US', 'Global', 'Europe')"],
            market_category: Annotated[str, "Market category or industry"]
        ) -> str:
            """Estimate total addressable market (TAM) and serviceable market"""
            # This is a placeholder - in production, integrate with market research APIs
            return f"""Market Size Estimation for {market_category}:
            
Target Audience: {target_audience}
Geography: {geography}

Estimated TAM (Total Addressable Market): $X billion
Estimated SAM (Serviceable Addressable Market): $Y billion
Estimated SOM (Serviceable Obtainable Market): $Z million

Note: These are rough estimates. For accurate data, consider:
- Industry reports (Gartner, IDC, Forrester)
- Government statistics
- Trade associations
- Competitor analysis
- Customer surveys

Recommendation: Conduct primary research to validate market size."""
        
        def analyze_competitors(
            industry: Annotated[str, "Industry or market segment"],
            key_players: Annotated[str, "Names of main competitors (comma-separated)"]
        ) -> str:
            """Analyze competitive landscape"""
            competitors = [c.strip() for c in key_players.split(",")]
            
            analysis = f"""Competitive Analysis - {industry}

Key Competitors: {', '.join(competitors)}

Analysis Framework:

1. Competitive Positioning:
   - Direct competitors: [List players with similar offerings]
   - Indirect competitors: [Alternative solutions]
   - Emerging threats: [New entrants, disruptors]

2. Strengths & Weaknesses:
   For each competitor, analyze:
   - Market share
   - Pricing strategy
   - Key features/differentiators
   - Customer base
   - Funding/resources

3. Market Gaps:
   - Underserved segments
   - Feature gaps
   - Service gaps
   - Pricing opportunities

4. Differentiation Strategy:
   - Unique value proposition
   - Competitive advantages
   - Barriers to entry

Recommendation: Use Porter's Five Forces and SWOT analysis for deeper insights."""
            
            return analysis
        
        def calculate_unit_economics(
            revenue_per_customer: Annotated[float, "Average revenue per customer per year"],
            acquisition_cost: Annotated[float, "Customer acquisition cost (CAC)"],
            gross_margin: Annotated[float, "Gross margin percentage (0-100)"]
        ) -> str:
            """Calculate unit economics and business viability metrics"""
            
            # Calculate key metrics
            ltv_simple = revenue_per_customer * 3  # Assuming 3-year customer lifetime
            ltv_to_cac = ltv_simple / acquisition_cost if acquisition_cost > 0 else 0
            payback_months = (acquisition_cost / (revenue_per_customer / 12)) if revenue_per_customer > 0 else 0
            gross_profit = revenue_per_customer * (gross_margin / 100)
            
            result = f"""Unit Economics Analysis:

Revenue Metrics:
- Annual Revenue per Customer: ${revenue_per_customer:,.2f}
- Customer Lifetime Value (3 yr): ${ltv_simple:,.2f}
- Annual Gross Profit per Customer: ${gross_profit:,.2f}

Cost Metrics:
- Customer Acquisition Cost (CAC): ${acquisition_cost:,.2f}
- Gross Margin: {gross_margin}%

Key Ratios:
- LTV:CAC Ratio: {ltv_to_cac:.2f}x
- CAC Payback Period: {payback_months:.1f} months

Viability Assessment:
"""
            
            if ltv_to_cac >= 3:
                result += "✅ EXCELLENT - LTV:CAC ratio is healthy (>3:1)\n"
            elif ltv_to_cac >= 2:
                result += "⚠️  ACCEPTABLE - LTV:CAC ratio is workable (2-3:1)\n"
            else:
                result += "❌ CONCERNING - LTV:CAC ratio is too low (<2:1)\n"
            
            if payback_months <= 12:
                result += "✅ GOOD - CAC payback under 12 months\n"
            elif payback_months <= 18:
                result += "⚠️  ACCEPTABLE - CAC payback 12-18 months\n"
            else:
                result += "❌ RISKY - CAC payback over 18 months\n"
            
            result += "\nRecommendations:\n"
            result += "- Focus on reducing CAC through organic channels\n"
            result += "- Increase LTV through upsells and retention\n"
            result += "- Optimize pricing strategy\n"
            result += "- Improve product-market fit\n"
            
            return result
        
        return [
            calculate_market_size,
            analyze_competitors,
            calculate_unit_economics
        ]
    
    async def evaluate_business_idea(self, idea: str, context: str = "") -> AsyncIterator[str]:
        """
        Evaluate a business idea for market viability
        
        Args:
            idea: Description of the business idea
            context: Additional context (target market, budget, timeline, etc.)
        
        Yields:
            Streamed response chunks
        """
        prompt = f"""Please evaluate the following business idea for market viability:

Business Idea: {idea}

Additional Context: {context if context else "None provided"}

Provide a comprehensive analysis including:
1. Market Opportunity Assessment
2. Competitive Landscape
3. Business Model Viability
4. Key Risks and Challenges
5. Go-to-Market Strategy Recommendations
6. Financial Projections (high-level)
7. Next Steps with Priorities

Be specific, actionable, and honest about both opportunities and challenges."""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text
    
    async def create_go_to_market_strategy(self, business_description: str) -> AsyncIterator[str]:
        """Create a go-to-market strategy"""
        prompt = f"""Create a comprehensive go-to-market strategy for:

{business_description}

Include:
1. Target Market Segmentation
2. Value Proposition
3. Pricing Strategy
4. Distribution Channels
5. Marketing & Sales Plan
6. Launch Timeline
7. Success Metrics
8. Budget Considerations"""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text
    
    async def analyze_risks(self, business_context: str) -> AsyncIterator[str]:
        """Analyze business risks and mitigation strategies"""
        prompt = f"""Analyze risks for this business and provide mitigation strategies:

{business_context}

Identify:
1. Market Risks
2. Competitive Risks
3. Financial Risks
4. Operational Risks
5. Technical Risks
6. Legal/Regulatory Risks

For each risk, provide:
- Likelihood (High/Medium/Low)
- Impact (High/Medium/Low)
- Mitigation Strategy
- Contingency Plan"""

        thread = self.agent.get_new_thread()
        
        async for chunk in self.agent.run_stream(prompt, thread=thread):
            if chunk.text:
                yield chunk.text


# CLI Interface
async def main():
    """Command-line interface for Business Strategist Agent"""
    import asyncio
    
    print("🎯 Business Strategist Agent")
    print("=" * 50)
    
    agent = BusinessStrategistAgent()
    
    print("\nWhat would you like to do?")
    print("1. Evaluate a business idea")
    print("2. Create go-to-market strategy")
    print("3. Analyze business risks")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n📝 Enter your business idea:")
        idea = input("> ").strip()
        print("\n📝 Additional context (target market, budget, etc.) - optional:")
        context = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Analysis:\n")
        
        async for chunk in agent.evaluate_business_idea(idea, context):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "2":
        print("\n📝 Describe your business:")
        description = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Go-to-Market Strategy:\n")
        
        async for chunk in agent.create_go_to_market_strategy(description):
            print(chunk, end="", flush=True)
        print("\n")
    
    elif choice == "3":
        print("\n📝 Describe your business context:")
        context = input("> ").strip()
        
        print("\n" + "=" * 50)
        print("🤖 Risk Analysis:\n")
        
        async for chunk in agent.analyze_risks(context):
            print(chunk, end="", flush=True)
        print("\n")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
