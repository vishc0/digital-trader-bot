# 🚀 Quick Start Guide

Welcome to your AI Agent System! This guide will get you up and running in 5 minutes.

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
# Make sure you're in the ai_agents directory
cd ai_agents

# Install required packages (--pre flag is REQUIRED)
pip install agent-framework-azure-ai --pre
pip install python-dotenv pydantic aiohttp requests
```

### Step 2: Get GitHub Token (Free!)

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it: `AI Agents Token`
4. Check the scope: **✓ model.inference** (or Full access to AI Models)
5. Click "Generate token"
6. Copy the token (starts with `github_pat_...`)

### Step 3: Set Environment Variable

**Windows PowerShell:**

```powershell
$env:GITHUB_TOKEN="github_pat_YOUR_TOKEN_HERE"
```

**Linux/Mac:**

```bash
export GITHUB_TOKEN="github_pat_YOUR_TOKEN_HERE"
```

**Optional - Make it permanent:**

Create a `.env` file in the `ai_agents` folder:

```bash
GITHUB_TOKEN=github_pat_YOUR_TOKEN_HERE
```

### Step 4: Run Your First Agent

```bash
python quick_start.py
```

## 🎯 What Can These Agents Do?

### 1. 💼 Business Strategist

**Evaluates business ideas and creates strategies**

Example:

```python
python -c "from agents.business_strategist import main; import asyncio; asyncio.run(main())"
```

- Market viability analysis
- Competitive landscape
- Go-to-market strategy
- Financial projections
- Risk assessment

### 2. 🔬 Research Analyst

**Deep research and comprehensive analysis**

Example:

```python
python -c "from agents.research_analyst import main; import asyncio; asyncio.run(main())"
```

- Market research
- Competitive analysis
- Trend identification
- Industry reports
- Data synthesis

### 3. 💻 Code Engineer

**Software development and automation**

Example:

```python
python -c "from agents.code_engineer import main; import asyncio; asyncio.run(main())"
```

- Code generation
- Debugging
- Automation scripts
- CI/CD pipelines
- Tech stack recommendations

### 4. 📊 Product Manager

**Product strategy and roadmaps**

- Product roadmaps
- Feature prioritization
- User stories
- Sprint planning
- Success metrics

### 5. 📢 Marketing Specialist

**Marketing strategy and growth**

- Marketing plans
- Content calendars
- Social media strategy
- SEO/SEM optimization
- Brand positioning

### 6. 💰 Sales & Operations

**Sales processes and operations**

- Sales funnels
- CRM strategies
- Customer outreach
- Process automation
- Operations workflows

### 7. 🎯 Orchestrator

**Coordinates all agents for complex tasks**

Example:

```python
python -c "from agents.orchestrator import main; import asyncio; asyncio.run(main())"
```

## 🎮 Usage Examples

### Example 1: Evaluate a Business Idea

```bash
python quick_start.py
# Select option 1
# Enter: "AI-powered meal planning app for busy professionals"
```

### Example 2: Complete Business Setup

```bash
python quick_start.py
# Select option 2
# Enter: "Online course platform for creative skills"
# Enter: 8 (weeks)
```

### Example 3: Research a Market

```bash
python quick_start.py
# Select option 3
# Enter: "Sustainable packaging trends in e-commerce 2025"
```

### Example 4: Build an Application

```bash
python quick_start.py
# Select option 4
# Enter: "REST API for task management with user authentication"
```

## 🔧 Programmatic Usage

You can also use the agents directly in your Python code:

```python
import asyncio
from agents.orchestrator import OrchestratorAgent

async def evaluate_my_idea():
    orchestrator = OrchestratorAgent()
    
    idea = "AI-powered fitness coaching app"
    context = "Target: millennials, Budget: $50k"
    
    print("Evaluating business idea...\n")
    async for chunk in orchestrator.run_business_evaluation(idea, context):
        print(chunk, end="", flush=True)

asyncio.run(evaluate_my_idea())
```

### Using Individual Agents

```python
from agents.business_strategist import BusinessStrategistAgent
from agents.research_analyst import ResearchAnalystAgent
from agents.code_engineer import CodeEngineerAgent

# Business evaluation
strategist = BusinessStrategistAgent()
async for response in strategist.evaluate_business_idea("My idea"):
    print(response, end="")

# Research
researcher = ResearchAnalystAgent()
async for response in researcher.research_topic("AI trends"):
    print(response, end="")

# Code generation
engineer = CodeEngineerAgent()
async for response in engineer.generate_code("Build a REST API", "python"):
    print(response, end="")
```

## 📊 Model Selection

The agents use different models optimized for their tasks:

| Agent | Model | Why |
|-------|-------|-----|
| Business Strategist | gpt-4.1 | Best reasoning for strategy |
| Research Analyst | gpt-4.1 | Superior analysis capabilities |
| Code Engineer | o3-mini | Specialized for coding |
| Product Manager | gpt-4.1-mini | Efficient for structured tasks |
| Marketing | gpt-4.1 | Creative and strategic |
| Sales & Ops | gpt-4.1-mini | Operational efficiency |
| Orchestrator | gpt-4.1 | Complex coordination |

**All models are FREE through GitHub Models!** (subject to rate limits)

## 🎓 Advanced Features

### Multi-Agent Workflows

The orchestrator can coordinate multiple agents:

```python
# Full business setup uses ALL 6 agents
async for response in orchestrator.run_complete_business_setup(
    business_idea="E-commerce platform",
    duration_weeks=12
):
    print(response, end="")
```

### Custom Workflows

Create your own workflows by combining agents:

```python
from agent_framework import GroupChatBuilder
from agents.business_strategist import BusinessStrategistAgent
from agents.research_analyst import ResearchAnalystAgent

# Create agents
strategist = BusinessStrategistAgent()
researcher = ResearchAnalystAgent()

# Build custom workflow
workflow = (
    GroupChatBuilder()
    .set_manager(manager_agent)
    .participants([strategist.agent, researcher.agent])
    .with_max_rounds(10)
    .build()
)

# Run workflow
async for event in workflow.run_stream("Analyze SaaS market"):
    if event.text:
        print(event.text, end="")
```

## 🐛 Troubleshooting

### "Configuration validation failed"

- Make sure you set GITHUB_TOKEN environment variable
- Check the token has `model.inference` scope
- Try generating a new token

### "Rate limit exceeded"

- GitHub Models has free tier rate limits
- Wait a few minutes and try again
- For production use, consider Microsoft Foundry (Azure AI)

### Import errors

- Make sure you installed: `pip install agent-framework-azure-ai --pre`
- The `--pre` flag is required (package is in preview)

### Agents not responding

- Check your internet connection
- Verify GitHub token is valid
- Try a simpler request first

## 🚀 Next Steps

1. ✅ **Try all 4 main workflows** in `quick_start.py`
2. 📚 **Read the full README** for detailed documentation
3. 🎨 **Customize agent prompts** in `config.py`
4. 🔧 **Build custom workflows** for your specific needs
5. 📊 **Add tracing** for debugging (see README)

## 💡 Tips for Best Results

### Writing Good Prompts

**Good:**

```
"Create a marketing strategy for a B2B SaaS product targeting 
small businesses in the healthcare industry. Focus on content 
marketing and LinkedIn outreach."
```

**Not ideal:**

```
"Marketing plan"
```

### Using Multiple Agents

For complex tasks, use the **Complete Business Setup** option (#2) which coordinates:

- Business Strategist: Market analysis
- Research Analyst: Competitive research
- Product Manager: Product roadmap
- Marketing Specialist: Marketing plan
- Sales & Operations: Sales process
- Code Engineer: Tech implementation

## 🎉 You're Ready

You now have a powerful AI agent system at your fingertips. Start with simple tasks and gradually explore more complex workflows.

**Need help?** Check the full README.md for comprehensive documentation.

**Want more?** Explore the code in the `agents/` directory to see how each agent works.

Happy building! 🚀
