import React from 'react'
import Dashboard from './components/Dashboard'
import Approval from './components/Approval'
import Orders from './components/Orders'
import Strategies from './components/Strategies'

export default function App() {
    return (
        <div className="app">
            <header>
                <h1>Digital Trader - Operator Console</h1>
            </header>
            <main>
                <section className="left">
                    <Dashboard />
                    <Approval />
                </section>
                <section className="right">
                    <Strategies />
                    <Orders />
                </section>
            </main>
        </div>
    )
}
