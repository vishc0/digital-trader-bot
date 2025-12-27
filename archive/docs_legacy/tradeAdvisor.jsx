import React, { useState, useEffect, useCallback } from 'react';
import { RefreshCw, Zap, TrendingUp, TrendingDown, Clock, MessageSquare, Check, X, Bell } from 'lucide-react';
import { firestore } from 'firebase/firestore'; // Placeholder import for structure

// --- Firebase and LLM API Configuration (Mandatory Setup) ---
// Note: In a real microservice environment, the LLM call would route through a dedicated backend service (like our proposed AI/LLM Context Service).
// Here, we simulate the LLM call for the chat interface.
const GEMINI_MODEL = 'gemini-2.5-flash-preview-09-2025';
const GEMINI_API_URL = (apiKey) => `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${apiKey}`;
const apiKey = ""; // Canvas environment will inject this key

// --- MOCK DATA STRUCTURES ---
const MOCK_TRADE_SUGGESTIONS = [
    {
        id: 1,
        ticker: 'AAPL',
        strategy: 'A1: Mean Reversion',
        action: 'BUY',
        confidence: 0.88,
        entryPrice: 185.50,
        currentPrice: 185.65,
        takeProfit: 192.00,
        stopLoss: 182.00,
        rationale: "RSI < 30 (oversold) and price is 2 ATR below 20-day SMA. High probability bounce expected toward mean.",
        timeframe: 'Swing (3-7 Days)',
        status: 'Pending Approval',
    },
    {
        id: 2,
        ticker: 'TSLA',
        strategy: 'A2: Trend Following',
        action: 'SHORT',
        confidence: 0.75,
        entryPrice: 220.10,
        currentPrice: 219.90,
        takeProfit: 205.00,
        stopLoss: 225.50,
        rationale: "Price broke 50-day SMA support. MACD crossover confirms bearish momentum. Entering a short position.",
        timeframe: 'Swing (5-10 Days)',
        status: 'Pending Approval',
    },
    {
        id: 3,
        ticker: 'BABA/JD',
        strategy: 'A3: Stat Arb (Pairs)',
        action: 'HEDGE',
        confidence: 0.92,
        entryPrice: 'N/A',
        currentPrice: 'N/A',
        takeProfit: 'Spread Zero',
        stopLoss: 'Z-Score 3.0',
        rationale: "BABA/JD Z-score hit +2.5. Suggesting Short BABA, Long JD to profit from mean reversion of the pair's spread.",
        timeframe: 'Swing (2-5 Days)',
        status: 'Pending Approval',
    },
];

const MOCK_CORRECTIVE_ACTION = {
    id: 4,
    tradeId: 1,
    ticker: 'AAPL',
    type: 'E1 Adjustment',
    oldSL: 182.00,
    newSL: 184.50,
    rationale: "The market volatility increased (VIX spike). Adjusting SL to a tighter, volatility-aware threshold (1.5x ATR from trade entry) to prioritize loss resilience. Requires user approval.",
    status: 'Pending Approval',
};

// --- UTILITY FUNCTIONS ---
const getStatusClasses = (status) => {
    switch (status) {
        case 'Pending Approval':
            return 'bg-yellow-500/20 text-yellow-600 border border-yellow-500';
        case 'Approved/Active':
            return 'bg-blue-500/20 text-blue-600 border border-blue-500';
        case 'Executed':
            return 'bg-green-500/20 text-green-600 border border-green-500';
        case 'Rejected':
            return 'bg-red-500/20 text-red-600 border border-red-500';
        default:
            return 'bg-gray-500/20 text-gray-600';
    }
};

const formatPrice = (price) => (typeof price === 'number' ? `$${price.toFixed(2)}` : price);
const getPnl = (current, entry, action) => {
    if (typeof current !== 'number' || typeof entry !== 'number') return 'N/A';
    const pnl = action === 'BUY' ? (current - entry) : (entry - current);
    return `${(pnl * 100 / entry).toFixed(2)}%`;
};

// --- CHAT MODULE (LLM Integration) ---
const ChatWindow = ({ strategies, onSuggestFeature }) => {
    const [messages, setMessages] = useState([
        { role: 'model', text: 'Hello! I am your AI Trading Assistant. How can I help you analyze a trade, interpret performance, or suggest a new platform feature?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    // Function to simulate the LLM call with context injection
    const callGeminiWithContext = useCallback(async (userPrompt) => {
        // 1. Context Injection: Provide the LLM with the live data context
        const strategyContext = strategies.map(s => (
            `Trade #${s.id} (${s.ticker}): Status=${s.status}, Strategy=${s.strategy}, Action=${s.action}, Rationale: ${s.rationale}`
        )).join('\n');

        const systemPrompt = `You are a helpful, expert algorithmic trading assistant and application designer. Analyze the user's query based on the current trade suggestions provided below. Be concise, professional, and focus only on trading advice or app design.
Current Trade Suggestions:
${strategyContext}`;

        const chatHistory = messages.map(msg => ({ role: msg.role === 'model' ? 'model' : 'user', parts: [{ text: msg.text }] }));
        chatHistory.push({ role: 'user', parts: [{ text: userPrompt }] });

        const payload = {
            contents: chatHistory,
            systemInstruction: { parts: [{ text: systemPrompt }] },
        };

        setIsLoading(true);
        try {
            const response = await fetch(GEMINI_API_URL(apiKey), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            const text = result.candidates?.[0]?.content?.parts?.[0]?.text || "Sorry, I encountered an API error or the response was blocked.";

            setMessages(prev => [...prev, { role: 'model', text }]);

            // Simple keyword detection for feature suggestion (Wisdom Builder feedback)
            if (text.toLowerCase().includes('design') || text.toLowerCase().includes('feature') || userPrompt.toLowerCase().includes('feature')) {
                onSuggestFeature(userPrompt, text);
            }

        } catch (error) {
            console.error('LLM API Error:', error);
            setMessages(prev => [...prev, { role: 'model', text: 'An unexpected system error occurred while contacting the AI service. Check the console for details.' }]);
        } finally {
            setIsLoading(false);
        }
    }, [messages, strategies, onSuggestFeature]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;
        const userPrompt = input;
        setMessages(prev => [...prev, { role: 'user', text: userPrompt }]);
        setInput('');
        callGeminiWithContext(userPrompt);
    };

    return (
        <div className="flex flex-col h-full bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden">
            <div className="p-3 bg-indigo-600 text-white font-bold text-lg flex items-center">
                <MessageSquare className="w-5 h-5 mr-2" /> AI Context & Chat Service
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4 text-sm">
                {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] p-3 rounded-xl shadow-md ${msg.role === 'user' ? 'bg-indigo-100 text-indigo-800 rounded-br-none' : 'bg-gray-100 text-gray-700 rounded-tl-none'}`}>
                            {msg.text}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="max-w-[80%] p-3 rounded-xl bg-gray-100 text-gray-700 animate-pulse">
                            AI Assistant is thinking...
                        </div>
                    </div>
                )}
            </div>
            <form onSubmit={handleSubmit} className="p-3 border-t">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Ask about a trade or suggest a feature..."
                    disabled={isLoading}
                />
                <button type="submit" className="hidden" />
            </form>
        </div>
    );
};

// --- MAIN APP COMPONENT ---
const App = () => {
    const [suggestions, setSuggestions] = useState(MOCK_TRADE_SUGGESTIONS);
    const [correctiveAction, setCorrectiveAction] = useState(MOCK_CORRECTIVE_ACTION);
    const [notifications, setNotifications] = useState([]);
    const [activeTab, setActiveTab] = useState('trades');

    // --- SEMI-AUTOMATION LOGIC ---
    const handleApproval = (id, isApproved, isCorrection = false) => {
        if (isCorrection) {
            if (isApproved) {
                setCorrectiveAction({ ...correctiveAction, status: 'Executed' });
                // Find the original trade and update its SL (simulated E1 learning)
                setSuggestions(prev => prev.map(s => s.id === correctiveAction.tradeId ? { ...s, stopLoss: correctiveAction.newSL } : s));
                setNotifications(prev => [...prev, { id: Date.now(), message: `Corrective action for ${correctiveAction.ticker} approved and new SL set to ${formatPrice(correctiveAction.newSL)}.` }]);
                setCorrectiveAction(null);
            } else {
                setCorrectiveAction({ ...correctiveAction, status: 'Rejected' });
                setNotifications(prev => [...prev, { id: Date.now(), message: `Corrective action for ${correctiveAction.ticker} rejected. SL remains at ${formatPrice(correctiveAction.oldSL)}.` }]);
            }
            return;
        }

        // Handle initial trade approval
        setSuggestions(prev => prev.map(s =>
            s.id === id ? { ...s, status: isApproved ? 'Approved/Active' : 'Rejected' } : s
        ));

        if (isApproved) {
            setNotifications(prev => [...prev, { id: Date.now(), message: `Trade ${id} (${suggestions.find(s => s.id === id).ticker}) approved. Execution pending...` }]);
        } else {
            setNotifications(prev => [...prev, { id: Date.now(), message: `Trade ${id} (${suggestions.find(s => s.id === id).ticker}) rejected by user.` }]);
        }
    };

    // --- LLM FEEDBACK FOR WISDOM BUILDER ---
    const handleSuggestFeature = (userPrompt, llmResponse) => {
        const feedback = {
            timestamp: new Date().toISOString(),
            userPrompt,
            llmResponse,
        };
        // In the microservice environment, this data would be sent to the AI/LLM Context Service
        // for ingestion by the Wisdom Builder/Feature Design Backlog.
        console.log("WISDOM BUILDER/FEATURE FEEDBACK RECEIVED:", feedback);
        setNotifications(prev => [...prev, { id: Date.now(), message: 'Feature idea logged to Wisdom Builder for future development.' }]);
    };


    return (
        <div className="min-h-screen bg-gray-50 font-sans p-6 md:p-10">
            <script src="https://cdn.tailwindcss.com"></script>
            <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .tab-button { transition: all 0.2s; }
      `}</style>

            <h1 className="text-4xl font-extrabold text-indigo-700 mb-6 flex items-center">
                <Zap className="w-8 h-8 mr-2 text-yellow-500" /> Adaptive Quant Trading Platform
            </h1>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* --- Left Column: Trade Overview & Actions --- */}
                <div className="lg:col-span-2 space-y-8">

                    {/* Tab Navigation */}
                    <div className="flex border-b border-gray-300 mb-4">
                        <button
                            className={`tab-button px-6 py-3 text-lg font-semibold ${activeTab === 'trades' ? 'text-indigo-600 border-b-4 border-indigo-600' : 'text-gray-500 hover:text-indigo-600'}`}
                            onClick={() => setActiveTab('trades')}
                        >
                            <Zap className="inline-block w-5 h-5 mr-2" /> Live Trade Suggestions
                        </button>
                        <button
                            className={`tab-button px-6 py-3 text-lg font-semibold ${activeTab === 'portfolio' ? 'text-indigo-600 border-b-4 border-indigo-600' : 'text-gray-500 hover:text-indigo-600'}`}
                            onClick={() => setActiveTab('portfolio')}
                        >
                            <TrendingUp className="inline-block w-5 h-5 mr-2" /> Portfolio & Risk (Mock)
                        </button>
                    </div>

                    {activeTab === 'trades' && (
                        <div className="space-y-6">
                            {/* --- CORRECTIVE ACTION PANEL (E1 & Risk Manager) --- */}
                            {correctiveAction && (
                                <div className="bg-red-50 border-2 border-red-500 p-5 rounded-xl shadow-lg animate-pulse">
                                    <div className="flex items-center justify-between mb-4">
                                        <h2 className="text-2xl font-bold text-red-700 flex items-center">
                                            <Bell className="w-6 h-6 mr-2 animate-wiggle" /> Corrective Action Suggested (E1)
                                        </h2>
                                        <span className={getStatusClasses(correctiveAction.status)}>{correctiveAction.status}</span>
                                    </div>
                                    <p className="text-gray-700 mb-3">
                                        <span className="font-semibold text-red-600">{correctiveAction.ticker}</span>: The live $P\&L$ has deviated significantly from the expected path due to a VIX spike. The Adaptive Optimizer suggests:
                                    </p>
                                    <div className="bg-white p-3 rounded-lg border border-red-300 mb-4 text-gray-800">
                                        <p>Change Stop-Loss from <span className="line-through text-red-500">{formatPrice(correctiveAction.oldSL)}</span> to <span className="text-green-600 font-bold">{formatPrice(correctiveAction.newSL)}</span> to increase loss resilience.</p>
                                    </div>

                                    <div className="flex space-x-4">
                                        <button
                                            onClick={() => handleApproval(null, true, true)}
                                            className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-xl shadow-md transition duration-150 transform hover:scale-[1.01] flex items-center justify-center"
                                        >
                                            <Check className="w-5 h-5 mr-2" /> Approve Correction
                                        </button>
                                        <button
                                            onClick={() => handleApproval(null, false, true)}
                                            className="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded-xl shadow-md transition duration-150 transform hover:scale-[1.01] flex items-center justify-center"
                                        >
                                            <X className="w-5 h-5 mr-2" /> Reject
                                        </button>
                                    </div>
                                </div>
                            )}

                            {/* --- TRADE SUGGESTION LIST --- */}
                            <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                                <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center justify-between">
                                    Trade Suggestions ({suggestions.length})
                                    <button className="text-indigo-500 hover:text-indigo-700 transition duration-150" onClick={() => setSuggestions(MOCK_TRADE_SUGGESTIONS)}><RefreshCw className="inline w-5 h-5 mr-1" /> Refresh Signals</button>
                                </h2>
                                <div className="space-y-4">
                                    {suggestions.map((trade) => (
                                        <div key={trade.id} className="bg-gray-50 p-4 rounded-lg border border-gray-200 shadow-sm transition duration-200 hover:shadow-md">
                                            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-center">
                                                <div>
                                                    <p className="text-sm font-medium text-gray-500">Ticker / Strategy</p>
                                                    <p className={`text-xl font-bold ${trade.action === 'BUY' ? 'text-green-600' : trade.action === 'SHORT' ? 'text-red-600' : 'text-yellow-600'}`}>{trade.ticker} ({trade.action})</p>
                                                    <span className="text-xs font-medium text-indigo-500">{trade.strategy}</span>
                                                </div>
                                                <div>
                                                    <p className="text-sm font-medium text-gray-500">Entry / Current Price</p>
                                                    <p className="text-lg font-semibold text-gray-800">{formatPrice(trade.entryPrice)} / {formatPrice(trade.currentPrice)}</p>
                                                    <p className={`text-sm font-bold ${getPnl(trade.currentPrice, trade.entryPrice, trade.action).includes('-') ? 'text-red-500' : 'text-green-500'}`}>{getPnl(trade.currentPrice, trade.entryPrice, trade.action)} P&L</p>
                                                </div>
                                                <div>
                                                    <p className="text-sm font-medium text-gray-500">Risk/Reward ($TP$/$SL$)</p>
                                                    <p className="text-sm text-gray-800">TP: {formatPrice(trade.takeProfit)}</p>
                                                    <p className="text-sm text-gray-800">SL: {formatPrice(trade.stopLoss)}</p>
                                                </div>
                                                <div className="flex flex-col items-end space-y-2">
                                                    <span className={getStatusClasses(trade.status)}>{trade.status}</span>
                                                    <span className="text-xs text-gray-500 flex items-center"><Clock className="w-3 h-3 mr-1" /> {trade.timeframe}</span>

                                                    {trade.status === 'Pending Approval' && (
                                                        <div className="flex space-x-2">
                                                            <button
                                                                onClick={() => handleApproval(trade.id, true)}
                                                                className="bg-green-500 hover:bg-green-600 text-white font-semibold px-3 py-1 rounded-md transition duration-150 transform hover:scale-105"
                                                                title="Approve Trade"
                                                            >
                                                                <Check className="w-4 h-4" />
                                                            </button>
                                                            <button
                                                                onClick={() => handleApproval(trade.id, false)}
                                                                className="bg-red-500 hover:bg-red-600 text-white font-semibold px-3 py-1 rounded-md transition duration-150 transform hover:scale-105"
                                                                title="Reject Trade"
                                                            >
                                                                <X className="w-4 h-4" />
                                                            </button>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                            <p className="text-xs italic text-gray-600 mt-2 border-t pt-2">Rationale: {trade.rationale}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'portfolio' && (
                        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Portfolio & Risk Metrics (Mock)</h2>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                                <div className="p-4 bg-indigo-50 rounded-lg">
                                    <p className="text-xl font-bold text-indigo-700">$100,000</p>
                                    <p className="text-sm text-gray-600">Total Capital</p>
                                </div>
                                <div className="p-4 bg-green-50 rounded-lg">
                                    <p className="text-xl font-bold text-green-700">12.5%</p>
                                    <p className="text-sm text-gray-600">Total $P\&L$ (YTD)</p>
                                </div>
                                <div className="p-4 bg-red-50 rounded-lg">
                                    <p className="text-xl font-bold text-red-700">-4.2%</p>
                                    <p className="text-sm text-gray-600">Max Drawdown</p>
                                </div>
                                <div className="p-4 bg-yellow-50 rounded-lg">
                                    <p className="text-xl font-bold text-yellow-700">1.85</p>
                                    <p className="text-sm text-gray-600">Sharpe Ratio</p>
                                </div>
                            </div>
                            <p className="mt-4 text-sm text-gray-600 border-t pt-4">Risk Management Status: <span className="font-semibold text-green-600">All positions within Max VaR (Value at Risk) limits.</span> The Circuit Breaker is active at -10% daily loss.</p>
                        </div>
                    )}
                </div>

                {/* --- Right Column: AI Chat and Notifications --- */}
                <div className="lg:col-span-1 flex flex-col space-y-6 h-[80vh]">
                    {/* AI Chat Component */}
                    <div className="flex-1 min-h-[50%]">
                        <ChatWindow strategies={suggestions} onSuggestFeature={handleSuggestFeature} />
                    </div>

                    {/* Notification Center */}
                    <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-800 mb-2">System Notifications ({notifications.length})</h3>
                        <div className="space-y-2 max-h-40 overflow-y-auto">
                            {notifications.slice(-5).reverse().map((n, index) => (
                                <div key={n.id} className={`p-2 text-xs rounded-md ${index === 0 ? 'bg-indigo-50 text-indigo-700 font-medium' : 'bg-gray-50 text-gray-600'}`}>
                                    {n.message}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default App;