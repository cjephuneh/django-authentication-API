# Django Authentication API

User Authentication APIs using Django Rest Framework (DRF).
It provides a flexible and secure users authentication endpoints for your Django applications.

### Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Sample API Request](#sample-api-request)
4. [API Endpoints](#api-endpoints)
5. [Installation](#installation)
6. [License](#license)

### Features

- Token-based authentication with Http-Cookies.
- Username or Email authentication.
- User registration and profile management.
- User login and logout functionality.
- User recover password with their email address.
- User reset email address to their new email.

### Prerequisites

- Git - [Download from Here](https://git-scm.com/downloads)
- Python - [Download from Here](https://www.python.org/downloads)

### Sample API Request

User Registration API

```http
POST /api/user/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "johndoe@example.com",
  "password": "John@1980"
}
```

User Login API

```http
POST /api/user/login/
Content-Type: application/json

{
  "username": "username_or_email",
  "password": "your_password"
}
```

### API Endpoints

<table>
  <thead>
    <tr>
      <th rowspan=2>API Endpoints</th>
      <th colspan=3 style='text-align:center'>User</th>
    </tr>
    <tr>
      <th>Anonymous User</th>
      <th>Authenticated User</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>api/user/register/</td>
      <td>POST</td>
      <td>-</td>
    </tr>
    <tr>
      <td>api/user/login/</td>
      <td>POST</td>
      <td>-</td>
    </tr>
    <tr>
      <td>api/user/logout/</td>
      <td>-</td>
      <td>GET</td>
    </tr>
    <tr>
      <td>api/user/account/confirm/token/</td>
      <td>POST</td>
      <td>-</td>
    </tr>
    <tr>
      <td>api/user/account/password/change/</td>
      <td>-</td>
      <td>UPDATE</td>
    </tr>
    <tr>
      <td>api/user/account/email/reset/</td>
      <td>-</td>
      <td>POST</td>
    </tr>
    <tr>
      <td>api/user/account/email/confirm/token/</td>
      <td>-</td>
      <td>UPDATE</td>
    </tr>
    <tr>
      <td>api/user/account/profile</td>
      <td>-</td>
      <td>GET, UPDATE</td>
    </tr>
    <tr>
      <td>api/user/forgot-password/</td>
      <td>POST</td>
      <td>POST</td>
    </tr>
    <tr>
      <td>api/user/reset-password/token/</td>
      <td>POST</td>
      <td>POST</td>
    </tr>
   </tbody>
</table>

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/anuraagnagar/django-authentication-API.git
```

#### 2. Change the directory.

```bash
cd django-authentication-API
```

#### 3. Create a virtual environment.

```bash
python -m venv venv
```

##### To activate:

```bash
source venv/bin/activate  # On MacOS/Linux
```

```bash
venv\Scripts\activate  # On Windows
```

#### 4. Install requirement dependencies.

```bash
pip install -r requirements.txt
```

Before running migrations and starting the development server, make sure to duplicate the `.env.example` file as `.env` in your project's root directory, and then fill all the necessary details for all the environment variables within the `.env` file."

#### 5. Run migrations.

```bash
python manage.py migrate
```

#### 6. Start the development server.

```bash
python manage.py runserver
```

Visit http://localhost:8000/ in your browser for access this application.

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/anuraagnagar/django-authentication-API/blob/main/LICENSE) file for details.

### Author

[Anurag Nagar](mailto:nagaranurag1999@gmail.com)