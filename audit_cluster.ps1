# Audit Cluster Resources
# Run this script to fetch CPU, RAM, and Disk info from your nodes.
# You will be prompted for the password ('scott') for each node.

$nodes = @(
    @{ Host = "tiger-3010.mammoth-manta.ts.net"; User = "tiger" },
    @{ Host = "tiger3-390.mammoth-manta.ts.net"; User = "tiger3" }
)

foreach ($node in $nodes) {
    Write-Host "`n----------------------------------------" -ForegroundColor Cyan
    Write-Host "Connecting to $($node.Host)..." -ForegroundColor Yellow
    
    # Command to run: System Info, Resources, Docker check, Top Processes
    $cmd = "echo '--- System ---'; cat /etc/os-release | grep PRETTY_NAME; echo '--- Resources ---'; echo 'CPU Cores:'; nproc; echo 'Memory:'; free -h; echo 'Disk Space:'; df -h /; echo '--- Docker Status ---'; docker --version || echo 'DOCKER NOT INSTALLED'; docker-compose --version || echo 'COMPOSE NOT INSTALLED'; echo '--- Top Memory Hogs ---'; ps aux --sort=-%mem | head -n 6"
    
    # Execute SSH (User must type password)
    ssh "$($node.User)@$($node.Host)" $cmd
}

Write-Host "`n----------------------------------------" -ForegroundColor Cyan
Write-Host "Audit Complete. Please copy the output above and share it with Antigravity." -ForegroundColor Green
