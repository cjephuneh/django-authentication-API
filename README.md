# Django Authentication API

User Authentication APIs using Django Rest Framework (DRF).
It provides a flexible and secure authentication endpoints for your Django applications.

### Features

- Token-based authentication with Http-Cookies.
- Username or Email authentication.
- User registration and profile management.
- User login and logout functionality.
- User recover password with their email address.

### Prerequisites

- Git - [Download from Here](https://git-scm.com/downloads)
- Python - [Download from Here](https://www.python.org/downloads)

### Sample API Request

User Registration Api

```http
POST /api/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "johndoe@example.com",
  "password": "John@1980"
}
```

User Login Api

```http
POST /api/login/
Content-Type: application/json

{
  "username": "username_or_email",
  "password": "strong_password"
}
```

### Installation

1. Clone the repository

```bash
git clone https://github.com/anuraagnagar/django-authentication-API.git
```

2. Change the directory.

```bash
cd django-authentication-API
```

3. Create a virtual environment.

```bash
python -m venv venv
```

To activate:

```bash
source venv/bin/activate  # On MacOS/Linux
```

```bash
venv\Scripts\activate  # On Windows
```

4. Install requirement dependencies.

```bash
pip install -r requirements.txt
```

Before running migrations and starting the development server, make sure to duplicate the `.env.example` file as `.env` in your project's root directory, and then fill all the necessary details for all the environment variables within the `.env` file."

5. Run migrations.

```bash
python manage.py migrate
```

6. Start the development server.

```bash
python manage.py runserver
```

Visit http://localhost:8000/ in your browser for access this app;ication.

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/anuraagnagar/django-authentication-API/blob/main/LICENSE) file for details.
