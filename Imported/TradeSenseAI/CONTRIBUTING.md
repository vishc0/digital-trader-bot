# Contributing to TradeSense AI

Thank you for your interest in contributing to TradeSense AI! We welcome contributions from the community.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/TradeSenseAI.git
   cd TradeSenseAI
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original/TradeSenseAI.git
   ```
4. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### iOS Development

1. Open `ios/TradeSenseAI.xcodeproj` in Xcode
2. Make your changes
3. Run tests: ⌘+U
4. Ensure code builds without warnings
5. Test on simulator and physical device if possible

### Backend Development

1. Activate virtual environment:
   ```bash
   cd backend
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. Make your changes
3. Run tests:
   ```bash
   pytest tests/
   ```
4. Check code formatting:
   ```bash
   black . --check
   flake8 .
   ```

### ML Model Development

1. Work in `ml_training/notebooks/` for experimentation
2. Move production code to `ml_training/` scripts
3. Document model architecture and performance metrics
4. Include evaluation results in PR description

## Coding Standards

### Swift (iOS)
- Follow [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- Use SwiftLint for linting (config in `.swiftlint.yml`)
- Write meaningful variable and function names
- Add comments for complex logic
- Write unit tests for view models and use cases

**Example:**
```swift
// Good
func calculateAIScore(for stock: Stock, using indicators: [TechnicalIndicator]) -> AIScore {
    // Calculate composite score from multiple factors
    let technicalScore = evaluateTechnicalIndicators(indicators)
    let sentimentScore = analyzeSentiment(stock.ticker)
    return AIScore(technical: technicalScore, sentiment: sentimentScore)
}

// Bad
func calc(s: Stock, i: [TechnicalIndicator]) -> AIScore {
    // ...
}
```

### Python (Backend)
- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use Black for code formatting (`black .`)
- Use type hints for function signatures
- Write docstrings for all public functions
- Write unit tests (pytest) for all endpoints and services

**Example:**
```python
# Good
def predict_stock_price(
    ticker: str,
    days_ahead: int = 7,
    model: Optional[LSTMModel] = None
) -> PredictionResult:
    """
    Predict future stock price using LSTM model.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        days_ahead: Number of days to predict (default: 7)
        model: Pre-trained model, or None to load default
        
    Returns:
        PredictionResult with predicted prices and confidence intervals
    """
    # Implementation
    pass

# Bad
def predict(t, d=7, m=None):
    pass
```

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no code change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(ai): Add LSTM price prediction model
fix(trading): Resolve order execution timeout issue
docs(readme): Update installation instructions
refactor(portfolio): Simplify position calculation logic
test(api): Add integration tests for watchlist endpoints
```

## Pull Request Process

1. **Update your branch** with latest upstream:
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request** on GitHub:
   - Use a clear, descriptive title
   - Reference any related issues (#123)
   - Describe what changed and why
   - Include screenshots for UI changes
   - Add test results for new features

4. **PR Review Checklist**:
   - [ ] Code follows project style guidelines
   - [ ] Tests pass (CI checks green)
   - [ ] Documentation updated if needed
   - [ ] No merge conflicts
   - [ ] Commits follow conventional format
   - [ ] PR description is clear and complete

5. **Address Review Feedback**:
   - Make requested changes
   - Push updates to the same branch
   - Respond to reviewer comments

6. **Merge**:
   - Requires at least 1 approval
   - All CI checks must pass
   - Maintainer will merge when ready

## Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/TradeSenseAI/discussions)
- Join our [Discord server](https://discord.gg/tradesenseai) (coming soon)
- Email: contribute@tradesenseai.com

Thank you for contributing! 🎉
