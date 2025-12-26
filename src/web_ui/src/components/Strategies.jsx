import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function Strategies() {
    const [strategies, setStrategies] = useState(null)

    useEffect(() => {
        async function fetch() {
            try {
                const res = await axios.get('/api/strategies')
                setStrategies(res.data && res.data.strategies)
            } catch (e) {
                console.error(e)
            }
        }
        fetch()
    }, [])

    if (!strategies) return <div className="card">Loading strategies...</div>

    return (
        <div className="card">
            <h2>Strategies</h2>
            <ul>
                {Object.keys(strategies).map(k => (
                    <li key={k}>
                        <strong>{k}</strong>
                        <div>Vector: {strategies[k].vector && strategies[k].vector.join(', ')}</div>
                        <div>Expected Value: {strategies[k].expected_value}</div>
                    </li>
                ))}
            </ul>
        </div>
    )
}
