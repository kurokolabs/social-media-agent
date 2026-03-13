module.exports = {
  apps: [{
    name: "kuroko-linkedin-agent",
    script: "main.py",
    interpreter: "python3",
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: "512M",
    restart_delay: 5000,
    max_restarts: 5,
    min_uptime: "10s",
    env: { NODE_ENV: "production", PYTHONUNBUFFERED: "1" },
    error_file: "./logs/pm2-error.log",
    out_file: "./logs/pm2-out.log",
    log_date_format: "YYYY-MM-DD HH:mm:ss Z",
    merge_logs: true
  }]
}
