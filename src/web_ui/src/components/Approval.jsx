import React, { useState } from 'react'
import axios from 'axios'

export default function Approval() {
    const [requester, setRequester] = useState('')
    const [reason, setReason] = useState('')
    const [requestId, setRequestId] = useState('')
    const [approver, setApprover] = useState('')
    const [status, setStatus] = useState(null)

    async function submitRequest() {
        try {
            const res = await axios.post('/api/trading/request-live', { requester_id: requester, reason })
            setRequestId(res.request_id || (res.data && res.data.request && res.data.request.request_id))
            setStatus('requested')
        } catch (e) {
            console.error(e)
        }
    }

    async function approve() {
        try {
            const res = await axios.post(`/api/trading/approve-live/${requestId}`, { approver_id: approver })
            setStatus(res.data && res.data.request_status)
        } catch (e) {
            console.error(e)
        }
    }

    return (
        <div className="card">
            <h2>Live Trading Approval</h2>
            <div>
                <input placeholder="Requester ID" value={requester} onChange={e => setRequester(e.target.value)} />
                <input placeholder="Reason" value={reason} onChange={e => setReason(e.target.value)} />
                <button onClick={submitRequest}>Request Live</button>
            </div>
            <div style={{ marginTop: 10 }}>
                <input placeholder="Request ID" value={requestId} onChange={e => setRequestId(e.target.value)} />
                <input placeholder="Approver ID" value={approver} onChange={e => setApprover(e.target.value)} />
                <button onClick={approve}>Approve</button>
            </div>
            <div>Status: {status}</div>
        </div>
    )
}
