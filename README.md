# Product Mini Web Application

A comprehensive Django web application demonstrating authentication, database operations, CRUD functionality, role-based access control, PDF generation, and a modern UI.

## ✅ Features Implemented

### Core Requirements

| Feature | Status | Description |
|---------|--------|-------------|
| **User Signup** | ✅ Complete | Registration with email, password, and role selection |
| **User Login** | ✅ Complete | Email-based authentication with session management |
| **Secure Password Hashing** | ✅ Complete | Django's built-in PBKDF2 password hasher |
| **Session-based Authentication** | ✅ Complete | Django sessions with login_required decorator |
| **Logout Functionality** | ✅ Complete | Secure session termination |
| **CRUD Operations** | ✅ Complete | Full Create, Read, Update, Delete for Products and Categories |
| **SQLite Database** | ✅ Complete | With proper Django ORM models |
| **Database Migrations** | ✅ Complete | Django migrations for all models |
| **Form for Data Submission** | ✅ Complete | Django Forms with validation |
| **Table View for Records** | ✅ Complete | Styled tables with Tailwind CSS |
| **Basic Validation** | ✅ Complete | Form validation with error messages |
| **Clean, Simple Layout** | ✅ Complete | Modern UI with Tailwind CSS |
| **PDF Generation (Single Record)** | ✅ Complete | Download PDF for individual product |
| **PDF Generation (Full Table)** | ✅ Complete | Download PDF report for all products |

### Bonus Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Search & Filtering** | ✅ Complete | Search by name/description, filter by category/status |
| **Pagination** | ✅ Complete | Page numbers with navigation controls |
| **Role-Based Access (Admin/User)** | ✅ Complete | Admins have full CRUD, Users have read-only access |

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 5.0+ |
| **Database** | SQLite |
| **Frontend** | Django Templates + Tailwind CSS |
| **PDF Generation** | ReportLab |
| **Authentication** | Django built-in auth system |
| **Form Handling** | Django Forms + django-widget-tweaks |

## 📁 Project Structure

```
Product/
├── products/           # Django project settings
│   ├── settings.py     # Main settings file
│   ├── urls.py         # Root URL configuration
│   └── wsgi.py         # WSGI application
├── accounts/           # Authentication app
│   ├── forms.py        # Register and Login forms
│   ├── views.py        # Auth views (register, login, logout)
│   └── templates/      # Login and Register templates
├── dashboard/          # Main application
│   ├── models.py       # Product and Category models
│   ├── views.py        # CRUD views + PDF export
│   ├── forms.py        # Product and Category forms
│   ├── utils.py        # PDF generation utilities
│   └── templates/      # Dashboard templates
├── theme/              # Tailwind CSS configuration
│   ├── templates/      # Base template
│   └── static_src/     # Tailwind source files
├── db.sqlite3          # SQLite database
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js + npm (for Tailwind CSS build)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Product
```

### Step 2: Create Virtual Environment

```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

> **Note**: If PowerShell blocks activation, run as Admin:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Database Migrations

```bash
python manage.py migrate
```

### Step 5: Build Tailwind CSS

Navigate to the theme static source directory:

```bash
cd theme/static_src
npm install
npm run dev
```

### Step 6: Start the Development Server

In a new terminal (from project root):

```bash
python manage.py runserver
```

Open your browser and navigate to: **http://127.0.0.1:8000/**

## 📖 Usage Guide

### Authentication

| Action | URL | Description |
|--------|-----|-------------|
| Register | `/accounts/register/` | Create new account with role selection (User/Admin) |
| Login | `/accounts/login/` | Login with email and password |
| Logout | `/accounts/logout/` | End current session |

### Role-Based Access

| Role | Permissions |
|------|-------------|
| **Admin** (`is_staff=True`) | Full CRUD access - can create, view, edit, delete products and categories |
| **User** (`is_staff=False`) | Read-only access - can only view products and categories, export PDFs |

### Dashboard & Products

| Feature | URL | Admin | User |
|---------|-----|-------|------|
| Dashboard | `/dashboard/` | ✅ Full access | ✅ View only |
| Product List | `/dashboard/products/` | ✅ Full CRUD | ✅ View only |
| Create Product | `/dashboard/products/create/` | ✅ | ❌ |
| View Product | `/dashboard/products/<id>/` | ✅ | ✅ |
| Edit Product | `/dashboard/products/<id>/update/` | ✅ | ❌ |
| Delete Product | `/dashboard/products/<id>/delete/` | ✅ | ❌ |

### Categories

| Feature | URL | Admin | User |
|---------|-----|-------|------|
| Category List | `/dashboard/categories/` | ✅ Full CRUD | ✅ View only |
| Create Category | `/dashboard/categories/create/` | ✅ | ❌ |
| Delete Category | `/dashboard/categories/<id>/delete/` | ✅ | ❌ |

### PDF Export

| Feature | URL | Description |
|---------|-----|-------------|
| Export All Products | `/dashboard/products/pdf/` | Download PDF report of all products |
| Export Single Product | `/dashboard/products/<id>/pdf/` | Download detailed PDF for one product |

### Search & Filtering

On the Product List page (`/dashboard/products/`):
- **Search**: Filter by product name or description
- **Category Filter**: Filter by product category
- **Status Filter**: Filter by stock status (In Stock, Low Stock, Out of Stock)

## 📸 Screenshots

### Dashboard (Admin View)
- Stats cards showing Total Products, In Stock, Out of Stock
- Products table with View, Edit, Delete actions
- Categories table with Delete action

### Dashboard (User View)
- Same stats cards
- Products table without Actions column
- Categories table without Actions column

### Registration
- Role selection dropdown (User/Admin)
- First name, Last name, Email, Password fields

### Login
- Email and Password fields
- Role badge displayed in navbar after login

## 🔒 Security Features

1. **Password Hashing**: Django's PBKDF2 with SHA256
2. **CSRF Protection**: All forms include CSRF tokens
3. **Session Security**: Secure session cookies
4. **Permission Checks**: `@login_required` and custom `@admin_required` decorators
5. **Input Validation**: Server-side form validation

## 📦 Dependencies

```
Django>=5.0
django-tailwind>=3.8.0
django-widget-tweaks>=1.5.0
Pillow>=10.0.0
reportlab>=4.4.0
```

## 🧪 Testing the Application

1. **Register as Admin**: Choose "Admin" role during registration
2. **Create Products**: Add products with name, price, category, stock
3. **Register as User**: Create another account with "User" role
4. **Test Permissions**: Verify User cannot see Add/Edit/Delete buttons
5. **Export PDF**: Download product reports as PDF

## 📝 License

This project is for educational purposes.
