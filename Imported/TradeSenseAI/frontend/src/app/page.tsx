export default function Home() {
    return (
        <main className="min-h-screen bg-slate-900 text-white">
            <div className="container mx-auto px-4 py-16">
                <div className="text-center">
                    <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
                        TradeSense AI
                    </h1>
                    <p className="text-xl text-slate-400 mb-8">
                        AI-Powered Stock & Options Trading Platform
                    </p>
                    <div className="flex gap-4 justify-center">
                        <a
                            href="/dashboard"
                            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors"
                        >
                            Launch Dashboard
                        </a>
                        <a
                            href="/auth/login"
                            className="px-6 py-3 bg-slate-800 hover:bg-slate-700 rounded-lg font-semibold transition-colors"
                        >
                            Sign In
                        </a>
                    </div>
                </div>

                <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="p-6 bg-slate-800 rounded-lg">
                        <div className="text-3xl mb-4">📊</div>
                        <h3 className="text-xl font-semibold mb-2">ORATS-Style Charts</h3>
                        <p className="text-slate-400">
                            Interactive trade builder with earnings overlays, IV tracking, and options activity visualization
                        </p>
                    </div>

                    <div className="p-6 bg-slate-800 rounded-lg">
                        <div className="text-3xl mb-4">🤖</div>
                        <h3 className="text-xl font-semibold mb-2">AI-Powered Analysis</h3>
                        <p className="text-slate-400">
                            LSTM price predictions, sentiment analysis, and dynamic exit strategies powered by machine learning
                        </p>
                    </div>

                    <div className="p-6 bg-slate-800 rounded-lg">
                        <div className="text-3xl mb-4">💎</div>
                        <h3 className="text-xl font-semibold mb-2">Advanced Options</h3>
                        <p className="text-slate-400">
                            Greeks tracking, IV surface visualization, payoff diagrams, and multi-leg strategy builder
                        </p>
                    </div>
                </div>
            </div>
        </main>
    )
}
