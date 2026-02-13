#!/bin/bash

# Database Setup Script for SmartAlloc

set -e

echo "Setting up SmartAlloc database..."

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install PostgreSQL first."
    exit 1
fi

# Database configuration
DB_NAME="${DB_NAME:-smartalloc}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"

echo "Creating database: $DB_NAME"

# Create database
psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "Database $DB_NAME already exists"

echo "Database setup complete!"
echo ""
echo "Next steps:"
echo "1. Run migrations: python manage.py migrate"
echo "2. Create superuser: python manage.py createsuperuser"
echo "3. Train ML model: python scripts/train_model.sh"
