#!/usr/bin/env bash

start_mysql_container() {
  docker run --name mysql-container \
    -e MYSQL_ROOT_PASSWORD=my-secret-pw \
    -p 3306:3306 \
    -v mysql-data:/var/lib/mysql \
    -d mysql:latest
  
  echo "MySQL container started. Wait a moment for it to initialize..."
  sleep 10
  
  docker exec -it mysql-container mysql -u root -pmy-secret-pw -e "CREATE DATABASE IF NOT EXISTS ecommerce_dashboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
  echo "Database 'ecommerce_dashboard' created."
}

connect_mysql() {
  docker exec -it mysql-container mysql -u root -p
}

generate_env_file() {
  cat > ../.env << EOL
# Database configuration
DATABASE_URL=mysql+pymysql://root:my-secret-pw@localhost:3306/ecommerce_dashboard
# You can change the above URL according to your MySQL configuration

# API settings
API_V1_STR=/api/v1
PROJECT_NAME="E-commerce Admin Dashboard API"
EOL
  echo ".env file created with Docker MySQL connection."
}

show_help() {
    echo "Database Commands"
    echo "----------------"
    echo "Usage: ./commands.sh [command]"
    echo ""
    echo "Available commands:"
    echo "  start     - Start MySQL in Docker container"
    echo "  connect   - Connect to MySQL shell"
    echo "  env       - Generate .env file with Docker connection"
    echo "  migrate   - Run database migrations"
    echo "  demo      - Generate demo data"
    echo "  help      - Show this help message"
}

if [[ $# -eq 0 ]]; then
    show_help
    exit 0
fi

COMMAND=$1

case $COMMAND in
    start)
        start_mysql_container
        ;;
    connect)
        connect_mysql
        ;;
    env)
        generate_env_file
        ;;
    migrate)
        echo "Running database migrations..."
        cd .. && alembic upgrade head
        ;;
    demo)
        echo "Generating demo data..."
        cd .. && python scripts/create_demo_data.py
        ;;
    help)
        show_help
        ;;
    *)
        echo "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac