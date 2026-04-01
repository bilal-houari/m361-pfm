# PreSkool Management System

This project is a school management system developed with Django. It provides a centralized platform for managing institutional data, including student and teacher profiles, curriculum mapping, and academic performance tracking.

## Technical Stack
- **Backend**: Django 6.x
- **Database**: SQLite
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript

## Prerequisites
- Python 3.10+
- pip (Python package installer)

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/bilal-houari/m361-pfm
cd m361-pfm
```

### 2. Configure Virtual Environment

#### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py migrate
```

### 5. Data Seeding (Required for Demo)
The system includes a comprehensive data seeder to populate the database with a complete school environment (Admins, Teachers, Students, Classes, Exams, and Results).

```bash
python manage.py seed_data
```

## Running the Application
To start the local development server, execute the following command:

```bash
python manage.py runserver
```

Once the server is running, the application can be accessed at `http://127.0.0.1:8000/`.

### Default Credentials (from Seeder)
After running the seeder, you can log in with the following accounts:

- **Administrator**:
  - **Email**: `admin@preskool.com`
  - **Password**: `password`
- **Teacher**:
  - **Email**: `teacher@preskool.com`
  - **Password**: `password`
- **Student**:
  - **Email**: `student@preskool.com`
  - **Password**: `password`

## Project Structure
- `users/`: Custom identity management and role-based authentication.
- `students/`: Student profiles and academic logs.
- `teachers/`: Personnel records and subject assignments.
- `classes/`: Grade levels and curriculum coordination.
- `exams/`: Assessment planning and grading metrics.
- `core/`: Shared mixins, services, and management commands.
- `static/`: Global CSS and JavaScript assets.
- `templates/`: Hierarchical UI layer.

## Screenshots
