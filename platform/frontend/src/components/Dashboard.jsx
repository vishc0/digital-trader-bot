import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function Dashboard() {
    const [snapshot, setSnapshot] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchSnapshot() {
            try {
                const res = await axios.get('/api/dashboard/snapshot')
                setSnapshot(res.data)
            } catch (e) {
                console.error(e)
            } finally {
                setLoading(false)
            }
        }
        fetchSnapshot()
    }, [])

    if (loading) return <div className="card">Loading dashboard...</div>
    if (!snapshot) return <div className="card">No data</div>

    return (
        <div className="card">
            <h2>Dashboard</h2>
            <p><strong>Daily PnL:</strong> {snapshot.daily_pnl && snapshot.daily_pnl.daily_pnl}</p>
            <p><strong>Circuit Breaker:</strong> {snapshot.circuit_breaker && snapshot.circuit_breaker.status}</p>
            <p><strong>Market Regime:</strong> {snapshot.market_state && snapshot.market_state.regime}</p>
            <h3>Recent Trades</h3>
            <ul>
                {snapshot.recent_trades && snapshot.recent_trades.trades && snapshot.recent_trades.trades.map(t => (
                    <li key={t.trade_id}>{t.trade_id} - {t.event_type || 'trade'}</li>
                ))}
            </ul>
        </div>
    )
}
