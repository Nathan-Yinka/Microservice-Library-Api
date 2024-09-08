# Library API Management System

## Description
This project provides a dual-service API system for library management. The system includes:
- **Frontend API**:  Allows library users to enroll, browse, and borrow books.
- **Backend/Admin API**: Enables administrators to manage books and monitor user activities.

The system uses RabbitMQ for inter-service communication and is containerized using Docker, ensuring easy deployment and scalability.

## Features
- **User Management**: Supports user enrollment and data management.
- **Book Management**: Administrators can add, update, and delete books.
- **Borrowing System**: Users can borrow and return books through the system.
- **Real-Time Updates**: Utilizes RabbitMQ for inter-service messaging.
- **Docker Integration**: Simplifies deployment and environment setup.

## Technologies
- **Django REST Framework**: For creating RESTful services.
- **RabbitMQ**: For handling messages between services.
- **PostgreSQL**: Used as the database for both services.
- **Docker**: For containerization and easy deployment.

## Architecture
The system uses a microservices architecture with the following components:
- **Frontend API**: Manages user-facing operations like book browsing and borrowing.
- **Backend/Admin API**: Handles administrative functions such as inventory and user management.
- **RabbitMQ**: Serves as the message broker between the two services, facilitating loose coupling and reliable communication.

## File Structure

```plaintext
├── README.md
├── adminapi
│   ├── Dockerfile
│   ├── adminapi
│   ├── api/
│   ├── entrypoint.sh
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.yaml
└── frontendapi
    ├── Dockerfile
    ├── api/
    ├── entrypoint.sh
    ├── frontendapi
    ├── manage.py
    └── requirements.txt
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.8 or higher

### Installation
Clone the repository and navigate into the project directory:
```bash
git clone https://github.com/Nathan-Yinka/Microservice-Library-Api.git
cd Microservice-Library-Api
```

Build and launch the containers:
```bash
docker-compose up --build
```

### Usage
Once the services are up and running, you can access:
- Frontend API at http://localhost:8001
- Backend/Admin API at http://localhost:8000


### API Documentation
Access the Swagger UI to view the API documentation and interact with the API endpoints:

- Frontend API Swagger: http://localhost:8001
- Admin API Swagger: http://localhost:8000

### Configuration
Environmental variables for configuring the system are located in the docker compose  file within the root folder

### Authors
- Oludare Nathaniel