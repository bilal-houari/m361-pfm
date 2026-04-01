# PreSkool Management System

> [!IMPORTANT]
> **Implementation Note**: This project utilizes a custom-built user interface rather than the provided Bootstrap template. This decision was made due to the technical complexity and file redundancy of the original assets, as detailed in **Section IV.2 Mise en œuvre du frontend et contraintes de templates** of the project report.
>
> **Project Repositories:**
> - **Part 1 (TP & Template Exploration)**: [m361/pfm-tp-guide](https://github.com/bilal-houari/m361/blob/main/pfm-tp-guide)
> - **Part 2 (Final Implementation)**: [m361-pfm](https://github.com/bilal-houari/m361-pfm)

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

## Screenshot<img width="1920" height="1033" alt="Screenshot_2026,04,01_18:59:55" src="https://github.com/user-attachments/assets/ba348fe2-1554-4445-a603-309626884c37" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:00:41" src="https://github.com/user-attachments/assets/680c8a0e-29b6-49e5-9773-0f9487c7a4ad" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:01:22" src="https://github.com/user-attachments/assets/f1ef40fe-15fa-411f-8ada-19c748b5f278" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:01:37" src="https://github.com/user-attachments/assets/9885539c-13e0-4868-b574-fb8b9db0c60a" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:02:08" src="https://github.com/user-attachments/assets/21ca0679-4b0b-4767-94d3-b7a7df79f3cd" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:02:19" src="https://github.com/user-attachments/assets/325faf0c-5fbc-45b3-a951-9548cfe3e1c3" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:02:29" src="https://github.com/user-attachments/assets/67b8095d-8787-46f4-91d5-3e4cdfc07835" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:02:47" src="https://github.com/user-attachments/assets/fbfd359c-af9c-46cf-b479-0f1dc83463f0" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:03:38" src="https://github.com/user-attachments/assets/33232774-48f4-4f6d-9b64-9a089041a1f4" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:03:57" src="https://github.com/user-attachments/assets/b0d754a9-fcf1-496c-afc3-10648c836492" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:04:08" src="https://github.com/user-attachments/assets/55c7e764-ac41-42e2-bed1-bedf2e66cb8f" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:04:18" src="https://github.com/user-attachments/assets/6d62e975-1b77-47e1-bce0-664fff28f995" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:04:30" src="https://github.com/user-attachments/assets/d0a28e18-6fb5-4a81-afa6-964bfb4d96f1" />
<img width="1920" height="1033" alt="Screenshot_2026,04,01_19:04:36" src="https://github.com/user-attachments/assets/5069afb8-1346-46d4-a9aa-96df0aef2f5c" />
s
