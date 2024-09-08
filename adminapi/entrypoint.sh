#!/bin/bash
# entrypoint.sh

set -e

# Function to check RabbitMQ availability
wait_for_rabbitmq() {
    echo "Checking RabbitMQ connection..."
    until python -c "import pika; pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))" &>/dev/null
    do
        echo "Waiting for RabbitMQ to start..."
        sleep 5
    done
}

# Run database migrations.
echo "Running admin api migrations"
python manage.py migrate

# Ensure RabbitMQ is available before starting the consumer and the server.
wait_for_rabbitmq

# Start the consumer in the background
echo "Starting the admin api consumer"
python manage.py consume_messages &

# Start the Django development server.
echo "Starting admin api development server"
python manage.py runserver 0.0.0.0:8000
