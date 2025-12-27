import React, { useState } from 'react'
import axios from 'axios'

export default function Orders() {
    const [order, setOrder] = useState({ ticker: 'AAPL', side: 'buy', qty: 1, price: 150.0, order_type: 'limit' })
    const [result, setResult] = useState(null)

    async function place() {
        try {
            const res = await axios.post('/api/orders/place', order)
            setResult(res.data)
        } catch (e) {
            console.error(e)
        }
    }

    return (
        <div className="card">
            <h2>Place Order</h2>
            <div>
                <input value={order.ticker} onChange={e => setOrder({ ...order, ticker: e.target.value })} />
                <select value={order.side} onChange={e => setOrder({ ...order, side: e.target.value })}>
                    <option value="buy">Buy</option>
                    <option value="sell">Sell</option>
                </select>
                <input type="number" value={order.qty} onChange={e => setOrder({ ...order, qty: parseInt(e.target.value) })} />
                <input type="number" value={order.price} onChange={e => setOrder({ ...order, price: parseFloat(e.target.value) })} />
                <button onClick={place}>Place</button>
            </div>
            <pre>{result && JSON.stringify(result, null, 2)}</pre>
        </div>
    )
}
