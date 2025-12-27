# Hybrid Deployment Guide (Local + Tailscale)

This is the definitive guide to deploying the Digital Trader Bot on your local hybrid cluster.

## 🏗 The Cluster Map

## 🏗 The Cluster Map

| Node | Hostname | IP | Role | Components Installed |
|------|----------|----|------|----------------------|
| **Node 1** | `tiger-3010` | `100.86.172.63` | **CORE** | • **Redis** (Database/Cache)<br>• **API Gateway** (Routing)<br>• **State Manager** (Risk/Circuit Breakers)<br>• **Data Handler** (Market Feeds)<br>• **Journaling Service** (Audit)<br>• **Web UI** (Frontend) |
| **Node 2** | `tiger3-390` | `100.88.127.85` | **MUSCLE** | • **Strategy Engine** (Technical Analysis)<br>• **Wisdom Builder** (AI Training/Optimization)<br>• **External Intelligence** (Gemini LLM Integration)<br>• **Execution Manager** (Broker Orders) |

## 🛡️ Disaster Recovery (Cloud Failover)

If your local nodes fail (power outage, hardware crash), you can rapidly restore operations on a cloud provider (AWS, GCP, Azure) using the **same** Docker configuration.

### Strategy: "Lift and Shift"

Since we use Docker Compose, the entire platform is portable.

### Recovery Steps

1. **Provision VM**: Spin up a standard Ubuntu VM (e.g., AWS `t3.large` or GCP `e2-standard-2`).
2. **Install Docker**: Run `curl -fsSL https://get.docker.com | sh`.
3. **Clone Repo**: `git clone <your-repo-url> .`
4. **Deploy**:
    * *Option A (All-in-One)*: Run `docker-compose -f docker-compose.primary.yml -f docker-compose.worker.yml up -d`.
    * *Option B (Split)*: If using 2 VMs, follow the standard Node 1 / Node 2 guide, updating IPs in `.env`.

### Data Backup via Redis

To ensure you don't lose open positions:

1. **Automated**: Configure a cron job on Node 1 to copy `/var/lib/docker/volumes/redis_data` to S3/Google Drive nightly.
2. **Manual**: `scp -r tiger-node1:/var/lib/docker/volumes/redis_data ./local_backup`

## 1. Network Setup (SSH)

Add the following to your `~/.ssh/config` file to enable easy access:

```ssh
Host tiger
    HostName tiger-3010.mammoth-manta.ts.net
    User tiger
    # Password: scott

Host tiger3
    HostName tiger3-390.mammoth-manta.ts.net
    User tiger3
    # Password: scott
```

## 2. Deploying the Core (Primary)

**Target**: `tiger` (Node 1)

1. SSH into the machine: `ssh tiger`
2. Clone/Update the repo: `git pull`
3. Create `.env`:

    ```bash
    WORKER_NODE_IP=100.88.127.85
    ```

4. Launch Services:

    ```bash
    docker-compose -f docker-compose.primary.yml up -d --build
    ```

## 3. Deploying the Muscle (Worker)

**Target**: `tiger3` (Node 2)

1. SSH into the machine: `ssh tiger3`
2. Clone/Update the repo: `git pull`
3. Create `.env`:

    ```bash
    PRIMARY_NODE_IP=100.86.172.63
    GEMINI_API_KEY=your_actual_key_here
    ```

4. Launch Services:

    ```bash
    docker-compose -f docker-compose.worker.yml up -d --build
    ```

## 4. Verification

* **Dashboard**: Open `http://100.86.172.63:3000` in your browser.
* **Port Check**: From Node 2, verify it can see Redis on Node 1: `telnet 100.86.172.63 6379`.
