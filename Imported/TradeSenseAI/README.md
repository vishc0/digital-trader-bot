# TradeSense AI

<div align="center">

![TradeSense AI Logo](docs/images/logo.png)

**AI-Powered iOS Stock & Options Trading Platform**

[![iOS](https://img.shields.io/badge/iOS-17.0+-000000?style=flat&logo=apple&logoColor=white)](https://www.apple.com/ios/)
[![Swift](https://img.shields.io/badge/Swift-5.9+-FA7343?style=flat&logo=swift&logoColor=white)](https://swift.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[Features](#features) • [Architecture](#architecture) • [Getting Started](#getting-started) • [Roadmap](#roadmap) • [Contributing](#contributing)

</div>

---

## 🚀 Overview

TradeSense AI is a next-generation iOS trading application that combines institutional-grade trading capabilities with cutting-edge artificial intelligence. Trade stocks and options while leveraging AI-powered analysis, predictions, and automated insights to make informed trading decisions.

### Key Highlights

- 🤖 **AI-Powered Analysis**: One-click trade analysis with ML-based opportunity scoring (0-100)
- 📊 **Advanced Charting**: TradingView-inspired charts with 60+ technical indicators
- 🎯 **Dynamic Exit Strategies**: AI continuously monitors positions and adjusts exit plans
- 📱 **Multi-Broker Support**: Connect Fidelity, Schwab, TD Ameritrade, E*TRADE, Interactive Brokers
- 🔍 **Stock Screener**: AI-generated categories showing 20%+ profit potential stocks
- 💼 **Options Trading**: Multi-leg strategies with Greeks, IV analysis, and probability calculators
- 🎓 **Education First**: Tooltip help system explains every complex term in plain English
- ⌚ **Apple Ecosystem**: Widgets, Apple Watch app, Siri integration, Dynamic Island

---

## ✨ Features

### Trading Capabilities
- **Stocks**: Market orders, limit orders, stop-loss, fractional shares, extended hours
- **Options**: Single and multi-leg strategies (spreads, straddles, iron condors, etc.)
- **Paper Trading**: Practice with virtual money before risking real capital
- **Multi-Account**: Aggregate portfolios across multiple brokerage accounts

### AI Intelligence
- **Trade Analysis**: ML models analyze 50+ factors to score opportunities (0-100)
- **Price Predictions**: LSTM neural networks forecast 1-day, 3-day, 7-day, 30-day movements
- **Sentiment Analysis**: FinBERT analyzes news, social media, earnings calls for sentiment
- **Exit Strategies**: Deep Q-Network adjusts stop-loss and targets based on position trajectory
- **Portfolio Health**: AI monitors risk and suggests rebalancing

### Research & Analysis
- **Interactive Charts**: Candlestick, line, bar charts with pinch-to-zoom and gestures
- **60+ Indicators**: RSI, MACD, Bollinger Bands, Fibonacci, moving averages, volume profile
- **News & Sentiment**: Real-time news feed with AI sentiment scoring (-100 to +100)
- **Analyst Ratings**: Aggregated ratings, price targets, recent upgrades/downgrades
- **Fundamentals**: P/E, EPS, revenue growth, margins, balance sheet, cash flow

### Watchlists & Screening
- **Multiple Watchlists**: Organize stocks by theme with drag-and-drop reordering
- **Stock Screener**: Pre-built AI screens (20%+ profit, momentum, undervalued growth)
- **Custom Filters**: Filter by market cap, P/E, volume, AI score, technical signals
- **Real-Time Updates**: WebSocket-powered live price updates

### User Experience
- **Beautiful UI**: Premium dark-mode design with glassmorphism and vibrant colors
- **Tooltip Help**: Info icon next to every complex term with beginner-friendly explanations
- **Biometric Auth**: Face ID / Touch ID for secure, instant login
- **Apple Integration**: Widgets, Apple Watch, Siri Shortcuts, SharePlay

---

## 🏗️ Architecture

### Tech Stack

**iOS App**
- Swift 5.9+ with SwiftUI
- MVVM + Clean Architecture
- Combine for reactive state management
- CoreData for local persistence
- Swift Charts + Custom components

**Backend Services**
- FastAPI (Python 3.11+)
- PyTorch for ML models
- PostgreSQL + TimescaleDB
- Redis for caching
- Docker + Kubernetes

**AI/ML Models**
- **LSTM**: Price prediction (PyTorch)
- **FinBERT**: Sentiment analysis (Transformers)
- **XGBoost**: Opportunity scoring
- **DQN**: Dynamic exit strategies (Reinforcement Learning)
- **Mean-Variance**: Portfolio optimization

**Third-Party APIs**
- Polygon.io (real-time market data)
- IEX Cloud (fundamentals, news)
- NewsAPI (financial news)
- Reddit & Twitter APIs (social sentiment)
- Broker APIs (Alpaca, Fidelity, Schwab, TD Ameritrade, E*TRADE, Interactive Brokers)

### Project Structure

```
TradeSenseAI/
├── ios/                    # iOS App (Swift/SwiftUI)
├── backend/                # Python Backend (FastAPI)
├── ml_training/            # ML Model Training
├── docs/                   # Documentation
├── scripts/                # Utility Scripts
└── .github/                # CI/CD Workflows
```

---

## 🚀 Getting Started

### Prerequisites

**For iOS Development:**
- macOS 13.0+ (Ventura or later)
- Xcode 15.0+
- iOS 17.0+ device or simulator
- Apple Developer account (for TestFlight/App Store)

**For Backend Development:**
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (recommended)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/TradeSenseAI.git
cd TradeSenseAI
```

#### 2. iOS App Setup
```bash
cd ios
# Install dependencies (if using CocoaPods or SPM)
# Open Xcode project
open TradeSenseAI.xcodeproj
```

#### 3. Backend Setup
```bash
cd backend
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run database migrations
python scripts/init_db.py

# Start development server
uvicorn api.main:app --reload
```

#### 4. ML Model Training (Optional)
```bash
cd ml_training
# Download historical data
python scripts/download_data.py

# Train LSTM price prediction model
python train_lstm.py --ticker SPY --epochs 100

# Train sentiment model (or use pre-trained FinBERT)
python train_sentiment.py
```

### Running the App

**iOS Simulator:**
1. Open `ios/TradeSenseAI.xcodeproj` in Xcode
2. Select target device (iPhone 15 Pro simulator)
3. Press ⌘+R to build and run

**Backend API:**
```bash
cd backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Access API docs at: `http://localhost:8000/docs`

---

## 🗺️ Roadmap

### Phase 1: MVP (Weeks 1-10) ✅ In Progress
- [x] Project setup and architecture
- [x] Planning and design documentation
- [ ] Authentication and biometric login
- [ ] Broker integration (Alpaca for MVP)
- [ ] Basic portfolio and watchlist
- [ ] AI analysis engine (LSTM, XGBoost)
- [ ] Stock trading (market and limit orders)
- [ ] TestFlight beta release

### Phase 2: Advanced Features (Weeks 11-18)
- [ ] Multi-broker support (5 brokers)
- [ ] Options trading with Greeks
- [ ] Advanced charting (60+ indicators)
- [ ] Stock screener with AI categories
- [ ] Dynamic exit strategy model (DQN)
- [ ] Paper trading mode
- [ ] App Store v1.0 release

### Phase 3: Full Rollout (Weeks 19-26)
- [ ] AI Coach chatbot (GPT-4)
- [ ] Education hub with courses
- [ ] Apple Watch app
- [ ] iOS Widgets and Dynamic Island
- [ ] Siri integration
- [ ] Social features (follow traders, share ideas)
- [ ] App Store v2.0 release

See [ROADMAP.md](docs/ROADMAP.md) for detailed sprint breakdown.

---

## 📖 Documentation

- [**User Guide**](docs/user_guide.md) - How to use TradeSense AI
- [**API Reference**](docs/api_reference.md) - Backend API documentation
- [**Architecture**](docs/architecture.md) - Technical architecture deep-dive
- [**Feature Specification**](docs/features_specification.md) - Complete feature list
- [**Screen Designs**](docs/screen_designs.md) - UI/UX design documentation
- [**Implementation Plan**](docs/implementation_plan.md) - Development roadmap
- [**Contributing Guide**](CONTRIBUTING.md) - How to contribute

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- **Swift**: Follow [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/) and use Black for formatting
- **Commits**: Use [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📊 Project Status

![GitHub stars](https://img.shields.io/github/stars/yourusername/TradeSenseAI?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/TradeSenseAI?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/TradeSenseAI)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/TradeSenseAI)

**Current Phase**: Phase 1 - MVP Development (Sprint 1)  
**Progress**: Foundation & Setup (Week 1 of 10)  
**Next Milestone**: Authentication & Account Linking (Week 3)

---

## ⚠️ Disclaimer

TradeSense AI is for educational and informational purposes only. Trading stocks and options involves substantial risk of loss and is not suitable for all investors. AI-generated recommendations are not guarantees of future performance. Past performance is not indicative of future results. Always do your own research and consult with a licensed financial advisor before making investment decisions.

The developers and contributors of TradeSense AI are not registered investment advisors and do not provide personalized investment advice. Use this software at your own risk.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

This project leverages several excellent open-source projects:

- [machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) - ML trading framework
- [FinBERT](https://github.com/ProsusAI/finBERT) - Financial sentiment analysis
- [TA-Lib](https://github.com/mrjbq7/ta-lib) - Technical analysis library
- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance data
- [Backtrader](https://github.com/mementum/backtrader) - Strategy backtesting

Special thanks to the open-source community for making this project possible.

---

## 📧 Contact

**Project Maintainer**: Your Name  
**Email**: your.email@example.com  
**Twitter**: [@yourusername](https://twitter.com/yourusername)  

**Project Link**: [https://github.com/yourusername/TradeSenseAI](https://github.com/yourusername/TradeSenseAI)

---

<div align="center">

Made with ❤️ by traders, for traders

**[⬆ back to top](#tradesense-ai)**

</div>
