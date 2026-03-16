module.exports = {
  apps: [
    {
      name: "kuroko-agent",
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
      error_file: "./logs/pm2-agent-error.log",
      out_file: "./logs/pm2-agent-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true
    },
    {
      name: "kuroko-api",
      script: "main_api.py",
      interpreter: "python3",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "512M",
      restart_delay: 3000,
      max_restarts: 5,
      min_uptime: "10s",
      env: { NODE_ENV: "production", PYTHONUNBUFFERED: "1" },
      error_file: "./logs/pm2-api-error.log",
      out_file: "./logs/pm2-api-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true
    },
    {
      name: "kuroko-celery",
      script: "worker",
      interpreter: "celery",
      args: "-A tasks.celery_app worker --loglevel=info --concurrency=2",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "512M",
      restart_delay: 5000,
      max_restarts: 5,
      min_uptime: "10s",
      env: { NODE_ENV: "production", PYTHONUNBUFFERED: "1" },
      error_file: "./logs/pm2-celery-error.log",
      out_file: "./logs/pm2-celery-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true
    }
  ]
}
