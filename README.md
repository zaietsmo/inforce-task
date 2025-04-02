# Lunch Voting System

A Django REST API for an internal service that helps employees decide where to have lunch. This system allows restaurants to upload daily menus and employees to vote for their preferred lunch option.

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
  - [With Docker](#with-docker)
  - [Manual Setup](#manual-setup)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Project Structure](#project-structure)
- [Development](#development)
- [Future Improvements](#future-improvements)

## Features

- **Authentication**: Secure JWT-based authentication system
- **Restaurant Management**: Create restaurants and manage their information
- **Menu Management**: Upload and update daily menus for restaurants
- **Employee Management**: Register employees and manage profiles
- **Voting System**: Allow employees to vote for their preferred lunch menu
- **Results**: Get real-time voting results for current day

## System Architecture

The system is built with a microservices approach using Django REST Framework:

- **Users App**: Handles user and employee management
- **Restaurants App**: Manages restaurants and their daily menus
- **Votes App**: Handles the voting logic and results

## Tech Stack

- **Backend**: Django 5.1 + Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL 17
- **Containerization**: Docker and Docker Compose
- **Testing**: PyTest with pytest-django
- **API Documentation**: Swagger UI and ReDoc via drf-yasg
- **Code Quality**: Flake8 for linting

## Setup Instructions

### With Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/zaietsmo/inforce-task.git
   cd inforce-task
   ```

2. Copy environment variables:

   ```bash
   cp .env-sample .env
   ```

3. Update the environment variables in `.env` as needed:

   ```
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database settings
   POSTGRES_DB=lunch_voting
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

4. Build and run the containers:

   ```bash
   docker-compose up -d
   ```

5. Create a superuser (optional):

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Access the API at http://localhost:8000/

### Manual Setup

1. Clone the repository
2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database and update settings
5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`

## Authentication

The API uses JWT authentication:

1. **Register an employee account**:

   ```
   POST /api/employees/
   ```

   Example request body:

   ```json
   {
     "user": {
       "username": "employee1",
       "email": "employee1@example.com",
       "password": "securepassword",
       "first_name": "John",
       "last_name": "Doe"
     },
     "department": "Engineering"
   }
   ```

2. **Obtain an access token**:

   ```
   POST /api/token/
   ```

   Example request body:

   ```json
   {
     "username": "employee1",
     "password": "securepassword"
   }
   ```

3. **Use the token in requests**:

   ```
   Authorization: Bearer <your-access-token>
   ```

4. **Refresh an expired token**:
   ```
   POST /api/token/refresh/
   ```
   Example request body:
   ```json
   {
     "refresh": "<your-refresh-token>"
   }
   ```

## API Endpoints

### Restaurants

- `GET /api/restaurants/` - List all restaurants
- `POST /api/restaurants/` - Create a new restaurant
- `GET /api/restaurants/{id}/` - Retrieve restaurant details
- `PUT /api/restaurants/{id}/` - Update restaurant information
- `DELETE /api/restaurants/{id}/` - Delete a restaurant
- `POST /api/restaurants/{id}/upload-menu/` - Upload a daily menu

### Menus

- `GET /api/menus/` - List all menus
- `GET /api/menus/{id}/` - Retrieve menu details
- `GET /api/menus/today/` - Get all menus for today

### Employees

- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Register a new employee
- `GET /api/employees/{id}/` - Retrieve employee details
- `PUT /api/employees/{id}/` - Update employee information
- `DELETE /api/employees/{id}/` - Delete an employee

### Votes

- `GET /api/votes/` - List all votes
- `POST /api/votes/` - Cast a vote for a menu
- `GET /api/votes/results/` - Get voting results for today
