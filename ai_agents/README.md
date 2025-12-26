# AI Agent System for Solopreneurs

A powerful multi-agent system designed to help solopreneurs with business strategy, research, development, and operations.

## 🚀 Quick Start

### Prerequisites

```bash
# Install required package (--pre flag is REQUIRED while Agent Framework is in preview)
pip install agent-framework-azure-ai --pre
```

### Setup GitHub Models (Free Tier)

1. Generate a GitHub Personal Access Token (PAT):
   - Go to <https://github.com/settings/tokens>
   - Create a new token with `model.inference` scope

2. Set environment variable:

   ```bash
   # Windows PowerShell
   $env:GITHUB_TOKEN="your_github_pat_here"
   
   # Linux/Mac
   export GITHUB_TOKEN="your_github_pat_here"
   ```

### Run Agents

```bash
# Business idea evaluation
python ai_agents/run_business_evaluator.py

# Research and analysis
python ai_agents/run_research_agent.py

# Coding assistance
python ai_agents/run_code_engineer.py

# Full solopreneur workflow
python ai_agents/run_solopreneur_workflow.py
```

## 🤖 Agent Personas

### 1. Business Strategist Agent

**Purpose**: Evaluate business ideas, assess market viability, create go-to-market strategies

**Capabilities**:

- Market analysis and competitive research
- Business model validation
- Revenue projections and financial planning
- Risk assessment
- Next-step action plans

**Model**: `openai/gpt-4.1` (strong reasoning for strategic thinking)

---

### 2. Research Analyst Agent

**Purpose**: Deep research on any topic with comprehensive documentation

**Capabilities**:

- Multi-source information gathering
- Data synthesis and analysis
- Trend identification
- Report generation with citations
- Executive summaries

**Model**: `openai/gpt-4.1` (excellent for analytical work)

---

### 3. Code Engineer Agent

**Purpose**: Software development, automation, and system management

**Capabilities**:

- Code generation and refactoring
- Debugging and testing
- CI/CD pipeline setup
- Remote system management
- Infrastructure as code

**Model**: `openai/o3-mini` (optimized for coding with reasoning)

---

### 4. Product Manager Agent

**Purpose**: Product strategy and development lifecycle

**Capabilities**:

- Product roadmap creation
- User story writing
- Feature prioritization
- Sprint planning
- Metrics and KPIs

**Model**: `openai/gpt-4.1-mini` (efficient for structured tasks)

---

### 5. Marketing Specialist Agent

**Purpose**: Marketing strategy, content creation, brand building

**Capabilities**:

- Content marketing strategies
- Social media planning
- SEO optimization
- Email campaigns
- Brand positioning

**Model**: `openai/gpt-4.1` (creative and strategic)

---

### 6. Sales & Operations Agent

**Purpose**: Customer acquisition, support, and business operations

**Capabilities**:

- Sales funnel optimization
- Customer outreach templates
- Operations automation
- Support documentation
- Process improvement

**Model**: `openai/gpt-4.1-mini` (efficient for operational tasks)

---

### 7. Orchestrator Agent

**Purpose**: Coordinates multi-agent workflows and task delegation

**Capabilities**:

- Task routing to specialist agents
- Workflow coordination
- Context management
- Result aggregation
- Conflict resolution

**Model**: `openai/gpt-4.1` (needs strong reasoning for orchestration)

---

## 📁 Project Structure

```
ai_agents/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config.py                          # Configuration and model settings
├── agents/
│   ├── __init__.py
│   ├── business_strategist.py        # Business evaluation agent
│   ├── research_analyst.py           # Research agent
│   ├── code_engineer.py              # Coding agent
│   ├── product_manager.py            # Product management agent
│   ├── marketing_specialist.py       # Marketing agent
│   ├── sales_operations.py           # Sales & ops agent
│   └── orchestrator.py               # Multi-agent orchestrator
├── tools/
│   ├── __init__.py
│   ├── web_search.py                 # Web search capabilities
│   ├── file_operations.py            # File I/O tools
│   ├── code_execution.py             # Code execution sandbox
│   └── api_client.py                 # API integrations
├── workflows/
│   ├── __init__.py
│   ├── business_evaluation.py        # Business idea evaluation workflow
│   ├── research_workflow.py          # Research workflow
│   └── solopreneur_workflow.py       # Full business operations workflow
├── run_business_evaluator.py         # CLI for business evaluation
├── run_research_agent.py             # CLI for research
├── run_code_engineer.py              # CLI for coding tasks
└── run_solopreneur_workflow.py       # CLI for complete workflow
```

## 🎯 Use Cases

### 1. Evaluate a Business Idea

```python
from ai_agents.workflows.business_evaluation import evaluate_business_idea

result = evaluate_business_idea(
    idea="AI-powered meal planning app for busy professionals",
    target_market="Urban professionals aged 25-45",
    budget=50000
)

print(result.viability_score)
print(result.action_plan)
print(result.risks)
```

### 2. Research a Topic

```python
from ai_agents.workflows.research_workflow import research_topic

report = research_topic(
    topic="Sustainable packaging trends in e-commerce",
    depth="comprehensive",
    include_citations=True
)

print(report.executive_summary)
print(report.key_findings)
```

### 3. Code Generation

```python
from ai_agents.agents.code_engineer import CodeEngineerAgent

agent = CodeEngineerAgent()
code = agent.generate_code(
    task="Create a REST API for user authentication with JWT",
    language="python",
    framework="FastAPI"
)

print(code)
```

### 4. Complete Solopreneur Workflow

```python
from ai_agents.workflows.solopreneur_workflow import run_business_sprint

# This orchestrates multiple agents working together
sprint = run_business_sprint(
    business_idea="Online course platform for creative skills",
    duration_days=30
)

print(sprint.product_roadmap)
print(sprint.marketing_plan)
print(sprint.sales_strategy)
```

## 🛠 Advanced Features

### Multi-Agent Collaboration

The orchestrator enables agents to work together:

```python
from ai_agents.agents.orchestrator import Orchestrator

orchestrator = Orchestrator()
result = orchestrator.execute_workflow(
    task="Launch a new SaaS product",
    agents=["business_strategist", "product_manager", "marketing_specialist", "code_engineer"]
)
```

### Custom Tools

Add custom tools to agents:

```python
from agent_framework.agents import Agent

def custom_api_call(endpoint: str) -> str:
    """Custom API integration"""
    # Your implementation
    pass

agent.add_tool(custom_api_call)
```

### Tracing and Observability

Track agent execution for debugging:

```python
from ai_agents.config import enable_tracing

enable_tracing()  # Automatically logs all agent interactions
```

## 📊 Why These Models?

| Model | Use Case | Reason |
|-------|----------|--------|
| `gpt-4.1` | Strategy, Research, Marketing | Superior reasoning and analysis |
| `gpt-4.1-mini` | Product Mgmt, Operations | Cost-effective for structured tasks |
| `o3-mini` | Code Generation | Best-in-class coding with reasoning |

## 🔐 Security Notes

- Never commit your GitHub PAT to version control
- Use environment variables for credentials
- Implement rate limiting for production use
- Validate all user inputs before processing

## 📚 Resources

- [Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [GitHub Models](https://github.com/marketplace/models)
- [Model Comparison Guide](https://github.com/marketplace/models)

## 🤝 Contributing

This is a personal agent system. Customize agents and workflows to fit your specific needs.

## 📝 License

This project uses the Apache 2.0 License for Agent Framework components.
