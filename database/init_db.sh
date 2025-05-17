#!/usr/bin/env bash

echo "Running MySQL initialization commands..."

if [[ -z "$1" ]]; then
    read -p "Enter MySQL username [root]: " MYSQL_USER
    MYSQL_USER=${MYSQL_USER:-root}
    
    read -s -p "Enter MySQL password: " MYSQL_PASSWORD
    echo ""
    
    read -p "Enter database name [ecommerce_dashboard]: " DB_NAME
    DB_NAME=${DB_NAME:-ecommerce_dashboard}
else
    MYSQL_USER=$1
    MYSQL_PASSWORD=$2
    DB_NAME=${3:-ecommerce_dashboard}
fi

echo "Creating database if it doesn't exist..."
mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -e "CREATE DATABASE IF NOT EXISTS $DB_NAME DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;"

echo "Updating .env file with database connection..."
cat > ../.env << EOL
DATABASE_URL=mysql+pymysql://$MYSQL_USER:$MYSQL_PASSWORD@localhost/$DB_NAME

API_V1_STR=/api/v1
PROJECT_NAME="E-commerce Admin Dashboard API"
EOL

echo "Database initialized successfully!"
