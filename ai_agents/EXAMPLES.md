# 🎯 AI Agent Use Cases & Examples

This guide shows practical examples of how to use your AI agents for real-world scenarios.

## 📋 Table of Contents

1. [Business Idea Evaluation](#1-business-idea-evaluation)
2. [Market Research & Analysis](#2-market-research--analysis)
3. [Building Software Products](#3-building-software-products)
4. [Solopreneur Business Operations](#4-solopreneur-business-operations)

---

## 1. Business Idea Evaluation

### Scenario: You have a business idea and want to validate it

**What you'll get:**

- Market size and opportunity analysis
- Competitive landscape assessment
- Financial viability analysis
- Go-to-market strategy
- Risk assessment
- Action plan with priorities

### Example Inputs

```
Business Idea: "AI-powered personal finance app for Gen Z"

Context: 
- Target: 18-25 year olds
- Budget: $75,000
- Timeline: 6 months to MVP
- Freemium model with $9.99/month premium
```

### How to Run

**Option 1: Quick Start (Interactive)**

```bash
python quick_start.py
# Select: 1 - Evaluate a business idea
```

**Option 2: Programmatic**

```python
import asyncio
from agents.business_strategist import BusinessStrategistAgent

async def evaluate():
    agent = BusinessStrategistAgent()
    
    idea = "AI-powered personal finance app for Gen Z"
    context = """
    Target: 18-25 year olds
    Budget: $75,000
    Timeline: 6 months to MVP
    Freemium model with $9.99/month premium
    """
    
    async for chunk in agent.evaluate_business_idea(idea, context):
        print(chunk, end="", flush=True)

asyncio.run(evaluate())
```

### Expected Output

- TAM/SAM/SOM analysis
- Competitor comparison (Mint, YNAB, etc.)
- Unit economics (LTV, CAC)
- Key risks and mitigation strategies
- 90-day action plan

---

## 2. Market Research & Analysis

### Scenario: Research a market before launching

**What you'll get:**

- Comprehensive market analysis
- Industry trends and projections
- Competitive intelligence
- Customer insights
- Opportunities and threats

### Example Use Cases

#### A. Industry Trend Analysis

```
Topic: "Sustainable e-commerce packaging trends 2025-2026"
```

#### B. Competitive Analysis

```
Topic: "Competitive analysis of meal kit delivery services: 
HelloFresh vs Blue Apron vs Home Chef"
```

#### C. Technology Research

```
Topic: "Best AI frameworks for building conversational agents: 
LangChain vs AutoGen vs Agent Framework"
```

### How to Run

```python
import asyncio
from agents.research_analyst import ResearchAnalystAgent

async def research():
    agent = ResearchAnalystAgent()
    
    # Trend analysis
    async for chunk in agent.trend_analysis(
        industry="Sustainable E-commerce",
        time_horizon="2025-2030"
    ):
        print(chunk, end="", flush=True)
    
    # OR competitive research
    async for chunk in agent.competitive_research(
        company_or_product="My SaaS product",
        competitors="Competitor A, Competitor B, Competitor C"
    ):
        print(chunk, end="", flush=True)

asyncio.run(research())
```

---

## 3. Building Software Products

### Scenario: You need to build software for your business

### Example A: REST API Development

```
Project: "User authentication API with JWT tokens"

Requirements:
- Python with FastAPI
- PostgreSQL database
- JWT authentication
- Rate limiting
- OpenAPI documentation
- Docker deployment
```

### Example B: Automation Script

```
Project: "Daily data backup automation"

Requirements:
- Backup PostgreSQL database
- Upload to AWS S3
- Email notification on success/failure
- Run daily at 2 AM
- Retention: keep last 30 days
```

### Example C: Complete Web Application

```
Project: "Task management web app"

Requirements:
- React frontend
- Node.js backend
- User authentication
- Real-time updates
- Mobile responsive
- Deploy to Vercel/Railway
```

### How to Run

```python
import asyncio
from agents.code_engineer import CodeEngineerAgent

async def build():
    agent = CodeEngineerAgent()
    
    task = """Create a REST API for user authentication with:
    - JWT token generation and validation
    - Password hashing with bcrypt
    - User registration and login endpoints
    - Password reset functionality
    - Rate limiting
    - OpenAPI/Swagger documentation
    """
    
    async for chunk in agent.generate_code(
        task=task,
        language="python",
        framework="FastAPI",
        requirements="Production-ready, with tests and deployment config"
    ):
        print(chunk, end="", flush=True)

asyncio.run(build())
```

---

## 4. Solopreneur Business Operations

### Scenario: You're launching a solopreneur business and need everything

**This is the ULTIMATE workflow** - uses ALL 6 specialist agents:

1. **Business Strategist**: Market analysis and strategy
2. **Research Analyst**: Market research and competitive intelligence
3. **Product Manager**: Product roadmap and features
4. **Marketing Specialist**: Marketing and growth strategy
5. **Sales & Operations**: Sales processes and operations
6. **Code Engineer**: Technical implementation

### Example: Complete Business Launch

```
Business: "Online course platform for creative professionals"

Timeline: 12 weeks

Requirements:
- Validate market opportunity
- Define MVP features
- Create go-to-market strategy
- Build marketing plan
- Setup sales processes
- Technical architecture
```

### How to Run

**Interactive:**

```bash
python quick_start.py
# Select: 2 - Complete business setup
```

**Programmatic:**

```python
import asyncio
from agents.orchestrator import OrchestratorAgent

async def launch_business():
    orchestrator = OrchestratorAgent()
    
    business_idea = """
    Online course platform for creative professionals
    
    Target Market:
    - Freelance designers, photographers, artists
    - 25-45 years old
    - Looking to monetize their expertise
    
    Business Model:
    - Monthly subscription: $29/month
    - Take 15% commission on course sales
    - Freemium with 1 free course
    
    Budget: $100,000
    Team: Solo founder (technical background)
    """
    
    async for chunk in orchestrator.run_complete_business_setup(
        business_idea=business_idea,
        duration_weeks=12
    ):
        print(chunk, end="", flush=True)

asyncio.run(launch_business())
```

### What You'll Get

**Week 1-2: Strategy & Research**

- Market size and opportunity
- Competitive analysis
- Customer personas
- Unique value proposition

**Week 3-4: Product Planning**

- Feature prioritization
- MVP definition
- Product roadmap
- Success metrics

**Week 5-6: Marketing Strategy**

- Brand positioning
- Marketing channels
- Content calendar (3 months)
- Customer acquisition strategy

**Week 7-8: Sales & Operations**

- Sales funnel design
- Email templates
- CRM strategy
- Operations workflows

**Week 9-12: Technical Implementation**

- Technology stack
- Architecture design
- Development plan
- Deployment strategy

---

## 🎓 Advanced Multi-Agent Workflows

### Custom Workflow Example

```python
import asyncio
from agent_framework import GroupChatBuilder
from agents.business_strategist import BusinessStrategistAgent
from agents.research_analyst import ResearchAnalystAgent
from agents.product_manager import ProductManagerAgent

async def custom_workflow():
    # Create agents
    strategist = BusinessStrategistAgent()
    researcher = ResearchAnalystAgent()
    product_manager = ProductManagerAgent()
    
    # Create manager for coordination
    from agent_framework.openai import OpenAIChatClient
    from openai import AsyncOpenAI
    from config import GITHUB_TOKEN, GITHUB_BASE_URL
    
    manager_client = OpenAIChatClient(
        async_client=AsyncOpenAI(
            base_url=GITHUB_BASE_URL,
            api_key=GITHUB_TOKEN,
        ),
        model_id="openai/gpt-4.1"
    )
    
    manager = manager_client.create_agent(
        name="Coordinator",
        instructions="Coordinate business planning workflow"
    )
    
    # Build workflow
    workflow = (
        GroupChatBuilder()
        .set_manager(manager, display_name="Coordinator")
        .participants([
            strategist.agent,
            researcher.agent,
            product_manager.agent
        ])
        .with_max_rounds(15)
        .build()
    )
    
    # Run workflow
    task = """
    Plan a mobile app for fitness coaching:
    1. Research market and competitors
    2. Evaluate business opportunity
    3. Create product roadmap
    """
    
    async for event in workflow.run_stream(task):
        if hasattr(event, 'text') and event.text:
            print(event.text, end="", flush=True)

asyncio.run(custom_workflow())
```

---

## 💡 Tips for Best Results

### 1. Be Specific

**Good:**

```
"Create a marketing strategy for a B2B SaaS product targeting 
small healthcare clinics. Focus on content marketing, LinkedIn 
outreach, and SEO. Budget: $5000/month"
```

**Not Great:**

```
"Marketing strategy"
```

### 2. Provide Context

Include:

- Target audience
- Budget constraints
- Timeline
- Existing resources
- Specific goals

### 3. Break Down Complex Tasks

For very complex projects:

1. Start with business evaluation
2. Then do detailed research
3. Then product planning
4. Then technical implementation

### 4. Iterate

Agents can refine their outputs:

```python
# First pass
result1 = await agent.evaluate_business_idea(idea, context)

# Refine based on initial results
result2 = await agent.evaluate_business_idea(
    idea, 
    f"{context}\n\nFocus more on: [specific aspect]"
)
```

---

## 🚀 Real-World Scenarios

### Scenario 1: Validating a Side Hustle

```bash
python quick_start.py
# Option 1: Evaluate business idea
# Input: "Selling custom 3D-printed planters on Etsy"
# Context: "Budget $2000, can produce 50/month, target price $30-50"
```

### Scenario 2: Pivoting Your Business

```bash
python quick_start.py
# Option 3: Research
# Input: "Market analysis for pivoting from B2C to B2B SaaS"
```

### Scenario 3: Technical Implementation

```bash
python quick_start.py
# Option 4: Build something
# Input: "Stripe payment integration for my subscription service"
```

### Scenario 4: Full Launch Plan

```bash
python quick_start.py
# Option 2: Complete business setup
# Input: "Newsletter platform for creators with monetization"
# Weeks: 8
```

---

## 🎯 Success Stories Template

Use this framework when working with agents:

1. **Define Your Goal**
   - What are you trying to achieve?
   - What's your timeline?
   - What resources do you have?

2. **Choose the Right Agent(s)**
   - Single agent for focused tasks
   - Orchestrator for complex projects

3. **Provide Rich Context**
   - The more details, the better results
   - Include constraints and requirements

4. **Review and Iterate**
   - Use agent output as a starting point
   - Refine with follow-up questions

5. **Take Action**
   - Implement recommendations
   - Track results
   - Come back for next phase

---

## 📞 Getting Help

Need assistance? The agents can help with:

- ❓ Clarifying questions
- 🔍 Deeper analysis
- 💡 Alternative approaches
- 📊 More detailed breakdowns

Just ask for what you need!

---

**Ready to build your business with AI?** Start with `quick_start.py` and explore! 🚀
