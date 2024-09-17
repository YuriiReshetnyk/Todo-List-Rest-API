# Todo List REST API

## Overview

The To-Do List application is a comprehensive tool built using Django and Django REST Framework, designed to manage and track tasks efficiently. The application is fully containerized using Docker and Docker Compose, ensuring a streamlined development and deployment process.

## Technologies Used

### Django 
A powerful Python web framework that promotes rapid development and clean, pragmatic design.

### Django REST Framework
A robust toolkit for building and managing Web APIs within Django applications.

### Docker 
A platform that enables the creation, deployment, and management of lightweight containers.

### Docker Compose 
A tool that simplifies the management of multi-container Docker applications using a single configuration file.

## Quickstart

### Clone this repository:
```
    git clone https://github.com/YuriiReshetnyk/Todo-List-Rest-API.git
```
### Build the images:
```
    docker-compose build
```
### Start the containers:
```
    docker-compose up
```
### If you want to run tests:
```
    docker-compose run --rm app sh -c "python manage.py test"
```

## Endpoints

1) GET [/api/schema]() <br>
- **description:** OpenApi3 schema for this API. <br>
- **body:**
```json
{
  "format": "yaml/json",
  "lang": "ua/en"
}
```
- **example of response:**
```json
openapi: 3.0.3
info:
  title: ''
  version: 0.0.0
paths:
  /api/shema/:
    get:
      operationId: shema_retrieve
      description: |-
        OpenApi3 schema for this API. Format can be selected via content negotiation.

        - YAML: application/vnd.oai.openapi
        - JSON: application/vnd.oai.openapi+json
      parameters:
      - in: query
        name: format
        schema:
          type: string
          enum:
          - json
          - yaml
      - in: query
... too long to be here )
```
2) GET [/api/task/tags]() <br>
- **description:** Return a list of tags of the authenticated user.<br>
- **params:** `assigned_only`(0/1) - return only tags that have tasks assigned to them if set to 1.  
- **body:**
```json
{
  "assigned_only": "0/1"
}
```
- **example of response:**
```json
[
    {
        "id": 2,
        "name": "Work"
    }
]
```

3) PUT [/api/task/tags/{id}/]() <br>
- **description:** Update a tag.<br>
- **body:**
```json
{
  "name": "Family"
}
```
- **example of response:**
```json
{
    "id": 2,
    "name": "Family"
}
```

4) PATCH [/api/task/tags/{id}/]() <br>
- **description:** Update a tag.<br>
- **body:**
```json
{
  "name": "Sport"
}
```
- **example of response:**
```json
{
    "id": 2,
    "name": "Sport"
}
```

5) DELETE [/api/task/tags/{id}/]() <br>
- **description:** Delete a tag.<br>

6) GET [/api/task/tasks/]() <br>
- **description:** Get a list of tasks.<br>
- **params**: *tags* - Comma seperated list of tag IDs to filter
- **body:**
```json
{
  "tags": "5"
}
```
- **example of response:**
```json
[
  {
    "id": 6,
    "created_at": "2024-09-16T19:52:01.516859+03:00",
    "description": "New task",
    "is_complete": true,
    "due_date": "2025-09-16T19:51:17.055000+03:00",
    "priority": 1,
    "tags": [
      {
        "id": 5,
        "name": "Family"
      }
    ]
  }
]
```

7) POST [/api/task/tasks/]() <br>
- **description:** Create and return a task.<br>
- **body:**
```json
{
  "description": "string",
  "due_date": "2025-09-17T08:03:32.764Z",
  "priority": 1,
  "tags": [
    {
      "name": "string"
    }
  ]
}
```
- **example of response:**
```json
{
  "id": 7,
  "created_at": "2024-09-17T11:04:44.939385+03:00",
  "description": "string",
  "is_complete": false,
  "due_date": "2025-09-17T11:03:32.764000+03:00",
  "priority": 1,
  "tags": [
    {
      "id": 6,
      "name": "string"
    }
  ]
}
```

8) GET [/api/task/tasks/{id}/]() <br>
- **description:** Return a task by its id.<br>
- **example of response:**
```json
{
  "id": 7,
  "created_at": "2024-09-17T11:04:44.939385+03:00",
  "description": "string",
  "is_complete": false,
  "due_date": "2025-09-17T11:03:32.764000+03:00",
  "priority": 1,
  "tags": [
    {
      "id": 6,
      "name": "string"
    }
  ]
}
```

9) PUT [/api/task/tasks/{id}/]() <br>
- **description:** Full update of a task.<br>
- **body:**
```json
{
  "description": "string",
  "is_complete": true,
  "due_date": "2024-11-17T08:08:19.401Z",
  "priority": 2,
  "tags": [
    {
      "name": "string123"
    }
  ]
}
```
- **example of response:**
```json
{
  "id": 7,
  "created_at": "2024-09-17T11:04:44.939385+03:00",
  "description": "string",
  "is_complete": true,
  "due_date": "2024-11-17T10:08:19.401000+02:00",
  "priority": 2,
  "tags": [
    {
      "id": 7,
      "name": "string123"
    }
  ]
}
```

10) PATCH [/api/task/tasks/{id}/]() <br>
- **description:** Partial update of a task.<br>
- **body:**
```json
{
  "tags": [
    {
      "name": "Family"
    }
  ]
}
```
- **example of response:**
```json
{
  "id": 7,
  "created_at": "2024-09-17T11:04:44.939385+03:00",
  "description": "string",
  "is_complete": true,
  "due_date": "2024-11-17T10:08:19.401000+02:00",
  "priority": 2,
  "tags": [
    {
      "id": 5,
      "name": "Family"
    }
  ]
}
```

10) DELETE [/api/task/tasks/{id}/]() <br>
- **description:** Delete a task by its ID.<br>

12) POST [/api/user/create/]() <br>
- **description:** Create a user in the system.<br>
- **body:**
```json
{
  "email": "user123@example.com",
  "password": "string123",
  "username": "string123"
}
```
- **example of response:**
```json
{
  "email": "user123@example.com",
  "username": "string123"
}
```

12) GET [/api/user/me/]() <br>
- **description:** Get an information about yourself.<br>
- **example of response:**
```json
{
  "email": "user123@example.com",
  "username": "string123"
}
```

13) PUT [/api/user/me/]() <br>
- **description:** Full update of your user profile.<br>
- **body:**
```json
{
  "email": "user1234@example.com",
  "password": "string1234",
  "username": "string1234"
}
```
- **example of response:**
```json
{
  "email": "user1234@example.com",
  "username": "string1234"
}
```

14) PATCH [/api/user/me/]() <br>
- **description:** Partial update of your user profile.<br>
- **body:**
```json
{
  "username": "YuriiReshetnyk"
}
```
- **example of response:**
```json
{
  "email": "user1234@example.com",
  "username": "YuriiReshetnyk"
}
```

14) PATCH [/api/user/me/]() <br>
- **description:** Partial update of your user profile.<br>
- **body:**
```json
{
  "username": "YuriiReshetnyk"
}
```
- **example of response:**
```json
{
  "email": "user1234@example.com",
  "username": "YuriiReshetnyk"
}
```

15) POST [/api/user/token/]() <br>
- **description:** Authenticate in the system. Return basic token.<br>
- **body:**
```json
{
  "email": "user1234@example.com",
  "password": "string1234"
}
```
- **example of response:**
```json
{
    "token": "3255dc81008442558886f7d5da5c5f0049cd44f7"
}
```