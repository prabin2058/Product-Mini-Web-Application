# Product Mini Web Application (Django)

A mini Django web application demonstrating:

- User authentication (register, login, logout)
- CRUD operations for Products (and basic Category management)
- Search/filtering and pagination for products
- TailwindCSS-based UI (via `django-tailwind` + `theme` app)

## Tech Stack

- Backend: Django
- Database: SQLite
- Frontend: Django Templates + TailwindCSS

## Project Structure

- `products/` Django project settings
- `accounts/` authentication (register/login/logout)
- `dashboard/` products & categories (CRUD)
- `theme/` Tailwind build pipeline and base template

## Setup (Windows)

### 1) Prerequisites

- Python 3.10+ (recommended)
- Node.js + npm (required for Tailwind build)

### 2) Create and activate a virtual environment

From the project root (where `manage.py` exists):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run PowerShell as Admin once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3) Install Python dependencies

If you have a `requirements.txt`, use:

```powershell
pip install -r requirements.txt
```

If you do not have a `requirements.txt` yet, install the core dependencies:

```powershell
pip install django django-tailwind django-widget-tweaks
```

### 4) Run migrations

```powershell
python manage.py migrate
```

(Optional) Create an admin user:

```powershell
python manage.py createsuperuser
```

### 5) Build TailwindCSS (required for styling)

Install Node packages:

```powershell
npm install
```

Run Tailwind in watch mode (recommended during development):

```powershell
npm run dev
```

Note: Run the above commands inside:

- `theme/static_src/`

### 6) Start the Django development server

In another terminal (project root):

```powershell
python manage.py runserver
```

Open:

- `http://127.0.0.1:8000/accounts/login/`

## How to Use

### Authentication

- Register: `/accounts/register/`
- Login: `/accounts/login/`
- Logout: `/accounts/logout/`

### Dashboard & Products

After login you can access:

- Dashboard: `/dashboard/`
- Product list: `/dashboard/products/`
- Add product: `/dashboard/products/create/`

Product List features:

- Search (name/description)
- Filter by category
- Filter by status
- Pagination (10 per page)

### Categories

- Category list: `/dashboard/categories/`
- Add category: `/dashboard/categories/create/`




