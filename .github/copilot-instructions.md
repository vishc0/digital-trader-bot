# GitHub Copilot Custom Instructions - AI Business Agents

This repository contains custom instructions for GitHub Copilot agents that help with business strategy, research, coding, and solopreneur operations.

## Available Agents

### 💼 @business-strategist
Expert in business strategy, market analysis, and viability assessment.

**Use when you need:**
- Business idea evaluation
- Market analysis and sizing
- Competitive landscape assessment
- Go-to-market strategy
- Financial projections and unit economics
- Risk assessment
- Strategic planning

**Example usage in Copilot Chat:**
```
@business-strategist Evaluate my SaaS idea: AI-powered task management for remote teams
```

---

### 🔬 @research-analyst
Expert in research, competitive analysis, and industry trends.

**Use when you need:**
- Market research and analysis
- Competitive intelligence
- Industry trend analysis
- Technology research
- Customer insights
- Data synthesis and reporting

**Example usage:**
```
@research-analyst Research sustainable packaging trends in e-commerce for 2025
```

---

### 💻 @code-architect
Expert in software development, architecture, and automation.

**Use when you need:**
- Code generation and architecture
- Debugging and optimization
- Technology stack recommendations
- Automation scripts
- CI/CD pipeline setup
- Infrastructure as code
- Best practices and design patterns

**Example usage:**
```
@code-architect Design a microservices architecture for a multi-tenant SaaS platform
```

---

### 📊 @product-strategist
Expert in product management, roadmaps, and feature prioritization.

**Use when you need:**
- Product roadmap creation
- Feature prioritization (RICE, MoSCoW)
- User story writing
- Sprint planning
- MVP definition
- Product metrics and KPIs
- Market fit analysis

**Example usage:**
```
@product-strategist Create a 6-month product roadmap for our mobile fitness app
```

---

### 📢 @growth-marketer
Expert in marketing strategy, growth tactics, and customer acquisition.

**Use when you need:**
- Marketing strategy and planning
- Content marketing and SEO
- Social media strategy
- Growth hacking techniques
- Customer acquisition channels
- Brand positioning
- Marketing analytics

**Example usage:**
```
@growth-marketer Create a content marketing strategy for a B2B SaaS product
```

---

### 💰 @sales-ops-expert
Expert in sales processes, operations, and CRM strategy.

**Use when you need:**
- Sales funnel design
- Lead generation strategies
- CRM implementation
- Sales playbooks
- Operations workflows
- Process automation
- Customer success strategies

**Example usage:**
```
@sales-ops-expert Design a sales funnel for a high-ticket coaching program
```

---

### 🎯 @business-orchestrator
Coordinates multiple expert agents for complex projects.

**Use when you need:**
- Complete business setup
- Multi-faceted projects
- Coordination across strategy, product, marketing, and tech
- End-to-end launch plans
- Complex decision making

**Example usage:**
```
@business-orchestrator Help me launch a new online course platform in 12 weeks
```

## How to Use These Agents

### In GitHub Copilot Chat

1. **Tag the agent** you want to use with `@agent-name`
2. **Describe your request** clearly and provide context
3. **Include specifics** like budget, timeline, target audience, etc.

### Example Workflows

#### Validating a Business Idea
```
@business-strategist Evaluate this idea: subscription box for eco-friendly home products. Target: urban millennials, budget $50k, looking for validation before building MVP.

@research-analyst Research the competitive landscape for subscription boxes in the sustainability space.

@product-strategist Define MVP features for a subscription box platform with curation and logistics.
```

#### Building a Feature
```
@code-architect I need to add real-time notifications to my React app. What's the best approach?

@code-architect Generate the WebSocket implementation for real-time notifications with fallback to polling.
```

#### Planning a Product Launch
```
@business-orchestrator Plan a 90-day launch for my SaaS product targeting small businesses.

@growth-marketer Create a pre-launch marketing strategy focused on content and partnerships.

@sales-ops-expert Design the sales process and CRM workflow for outbound B2B sales.
```

## Tips for Best Results

### 1. Be Specific
**Good:** 
```
@business-strategist Evaluate a meal planning app targeting busy professionals aged 25-40 
with household income $75k+. Freemium model with $12.99/month premium tier. Budget: $80k, 
timeline: 6 months to launch.
```

**Not ideal:**
```
@business-strategist What do you think of my app idea?
```

### 2. Provide Context
Include:
- Target audience/market
- Budget and timeline
- Current situation
- Constraints or requirements
- Specific goals

### 3. Use the Right Agent
- **Single focused task?** Use a specific agent
- **Complex project?** Use @business-orchestrator
- **Multiple perspectives?** Tag multiple agents in sequence

### 4. Iterate and Refine
Follow up with:
```
Can you elaborate on [specific aspect]?
How would this change if [different constraint]?
Show me code/examples for [specific part]?
```

## Agent Capabilities Matrix

| Agent | Strategy | Research | Code | Product | Marketing | Sales |
|-------|----------|----------|------|---------|-----------|-------|
| @business-strategist | ✓✓✓ | ✓✓ | - | ✓ | ✓ | ✓ |
| @research-analyst | ✓ | ✓✓✓ | - | ✓ | ✓✓ | ✓ |
| @code-architect | - | - | ✓✓✓ | ✓ | - | - |
| @product-strategist | ✓ | ✓ | ✓ | ✓✓✓ | ✓ | ✓ |
| @growth-marketer | ✓ | ✓✓ | - | ✓ | ✓✓✓ | ✓✓ |
| @sales-ops-expert | ✓ | ✓ | - | ✓ | ✓✓ | ✓✓✓ |
| @business-orchestrator | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ |

✓✓✓ = Primary expertise | ✓✓ = Strong capability | ✓ = Supporting capability

## Real-World Scenarios

### Scenario 1: Starting a Side Hustle
```
@business-strategist I want to start a side hustle selling digital templates on Etsy. 
Investment: $500, time: 10 hrs/week. Is this viable?

@research-analyst What are the top-selling template categories on Etsy in 2025?

@growth-marketer How do I market digital products on Etsy with minimal budget?
```

### Scenario 2: Building a SaaS Product
```
@business-orchestrator I want to build a project management tool for creative agencies. 
Timeline: 6 months, budget: $100k, solo technical founder.

@code-architect What's the best tech stack for a collaborative PM tool with real-time updates?

@product-strategist Define the MVP features that would make us competitive against Asana/Monday.

@growth-marketer Create a pre-launch strategy to get 100 beta users.
```

### Scenario 3: Scaling Operations
```
@sales-ops-expert We're growing from 5 to 50 customers/month. How do we scale our 
sales process without hiring?

@sales-ops-expert Create a CRM workflow for automated lead nurturing and qualification.

@code-architect Build an automation to sync leads from our website to CRM and trigger 
follow-up sequences.
```

## Advanced Usage

### Chaining Agents
```
@research-analyst Research AI coding assistant market size and trends

[Review research output]

@business-strategist Based on this research, evaluate the opportunity for a 
niche coding assistant for Python data scientists

[Review strategy]

@product-strategist Create a product roadmap for this coding assistant MVP

[Review roadmap]

@code-architect Design the technical architecture for this system

[Review architecture]

@growth-marketer Create a go-to-market plan targeting data science teams
```

### Collaborative Problem Solving
```
I need to decide between two business models for my app:
1. Subscription ($9.99/month)
2. One-time purchase ($49.99)

@business-strategist Analyze the pros/cons and financial implications of each model

@product-strategist How would each model affect product development priorities?

@growth-marketer Which model is easier to market to our target audience (hobby photographers)?

@sales-ops-expert Which model is easier to operationalize as a solo founder?
```

## Repository Setup

These custom instructions work across all repositories where you're logged in with your GitHub account.

### For Project-Specific Customization

Create a `.github/copilot-instructions.md` in your repository to add project-specific context:

```markdown
# Project-Specific Context

This is a [project description]

Key technologies: [tech stack]
Target users: [audience]
Business model: [model]
Current phase: [MVP/Growth/Scale]

When providing advice, consider these project specifics.
```

## Getting Help

If agents aren't responding as expected:

1. **Be more specific** - Add details about your situation
2. **Break down requests** - Large requests into smaller parts
3. **Provide examples** - Show what you're looking for
4. **Set constraints** - Budget, time, resources, technical level

## Updates and Feedback

These agent instructions are continuously improved. Feedback welcome!

---

**Ready to accelerate your business with AI agents?** Start by tagging the agent you need in Copilot Chat! 🚀
