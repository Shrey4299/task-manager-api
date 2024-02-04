# 🚀 Task Manager API Documentation

## 🛠️ Framework

This project utilizes Django and Django REST framework to provide a robust and scalable API for task management.

## 🗄️ Database Schema

The application uses an SQLite database with two tables:

### Table: `Task`

This table stores task information.

- `id`: Integer, Primary Key, Auto Increment
- `title`: String(255), Not Null
- `description`: Text
- `due_date`: DateTime
- `status`: String(20), Default: 'Pending'
- `created_at`: DateTime, Auto-Generated
- `user`: ForeignKey to `RegisterUser`, on_delete=models.CASCADE

### Table: `RegisterUser`

This table stores user information.

- `id`: Integer, Primary Key, Auto Increment
- `username`: String(150), Unique, Not Null
- `email`: String(100), Unique, Not Null
- `password`: String(100), Not Null
- `phone_number`: Integer, Not Null

## 🚀 Instructions to Run the Code

Before running the code, ensure that you have the following installed on your system:

- Python (3.x recommended)
- Django

### Installation
1. Install Python (version 3.7 or higher) on your system.
2. Clone this repository to your local machine: `git clone https://github.com/shrey4299/task-manager-api.git`
3. Navigate to the project directory: `cd task-manager-api`
4. Install the project dependencies: `pip install -r requirements.txt`
5. Apply the migrations to create the necessary database tables: `python manage.py migrate`
6. Start the Django development server: `python manage.py runserver`
7. The API will now be accessible at http://127.0.0.1:8000/.

Now you're ready to manage your tasks and users! 🚀

## 🚀 API Documentation

Below are the endpoints available in the `users` app:

### 1. **`/user/create/`**
   - **Method:** `POST`
   - **Description:** Create a new user.
   - **Request Body:**
     ```json
     {
       "username": "string",
       "email": "string",
       "password": "string",
       "full_name": "string",
       "age": 25,
       "gender": "string"
     }
     ```
   - **Response:** 
     ```json
     {
       "id": 1,
       "username": "string",
       "email": "string",
       "full_name": "string",
       "age": 25,
       "gender": "string"
     }
     ```
   
### 2. **`/user/<int:user_id>/`**
   - **Method:** `GET`
   - **Description:** Get user details by user ID.
   - **Response:** 
     ```json
     {
       "id": 1,
       "username": "string",
       "email": "string",
       "full_name": "string",
       "age": 25,
       "gender": "string"
     }
     ```

### 3. **`/user/<int:user_id>/`**
   - **Method:** `PUT`
   - **Description:** Update user details by user ID.
   - **Request Body:**
     ```json
     {
       "username": "string",
       "email": "string",
       "full_name": "string",
       "age": 26,
       "gender": "string"
     }
     ```
   - **Response:** 
     ```json
     {
       "message": "User updated successfully."
     }
     ```

### 4. **`/user/<int:user_id>/`**
   - **Method:** `DELETE`
   - **Description:** Delete user by user ID.
   - **Response:** 
     ```json
     {
       "message": "User deleted successfully."
     }
     ```

### 5. **`/user/reset-password/<int:user_id>/`**
   - **Method:** `POST`
   - **Description:** Reset user password by user ID.
   - **Request Body:**
     ```json
     {
       "new_password": "string"
     }
     ```
   - **Response:** 
     ```json
     {
       "message": "Password reset successfully."
     }
     ```

### 6. **`/user/login/`**
   - **Method:** `POST`
   - **Description:** Login user and get JWT token.
   - **Request Body:**
     ```json
     {
       "email": "string",
       "password": "string"
     }
     ```
   - **Response:** 
     ```json
     {
       "jwt": "string",
       "id": 1
     }
     ```

### 7. **`/user/logout/`**
   - **Method:** `POST`
   - **Description:** Logout user and clear JWT token.
   - **Response:** 
     ```json
     {
       "message": "success"
     }
     ```

## 🚀 Task API Documentation

Below are the endpoints available in the `tasks` app:

### 1. **`/api/tasks/`**
   - **Method:** `GET`
   - **Description:** Get all tasks grouped by status for the authenticated user.
   - **Response:** 
     ```json
     {
       "To Do": [...],
       "In Progress": [...],
       "Completed": [...]
     }
     ```

   - **Method:** `POST`
   - **Description:** Create a new task for the authenticated user.
   - **Request Body:**
     ```json
     {
       "title": "string",
       "description": "string",
       "status": "string"
     }
     ```
   - **Response:** 
     ```json
     {
       "id": 1,
       "title": "string",
       "description": "string",
       "status": "string"
     }
     ```

### 2. **`/api/tasks/<int:task_id>/`**
   - **Method:** `GET`
   - **Description:** Get details of a specific task for the authenticated user.
   - **Response:** 
     ```json
     {
       "id": 1,
       "title": "string",
       "description": "string",
       "status": "string"
     }
     ```

   - **Method:** `PUT`
   - **Description:** Update details of a specific task for the authenticated user.
   - **Request Body:**
     ```json
     {
       "title": "string",
       "description": "string",
       "status": "string"
     }
     ```
   - **Response:** 
     ```json
     {
       "id": 1,
       "title": "string",
       "description": "string",
       "status": "string"
     }
     ```

   - **Method:** `DELETE`
   - **Description:** Delete a specific task for the authenticated user.
   - **Response:** 
     ```json
     {
       "detail": "Task successfully deleted."
     }
     ```

### 3. **`/api/tasks/search/`**
   - **Method:** `GET`
   - **Description:** Search tasks based on status and/or title for the authenticated user.
   - **Query Parameters:**
     - `status` (optional): Filter tasks by status (e.g., "To Do", "In Progress", "Completed").
     - `title` (optional): Filter tasks by title (case-insensitive).
   - **Response:** 
     ```json
     [
       {
         "id": 1,
         "title": "string",
         "description": "string",
         "status": "string"
       },
       ...
     ]
     ```


