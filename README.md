# ConstructLink v1

ConstructLink is a Django web platform for Tanzania construction services. It connects equipment owners, contractors, drivers, logistics partners, construction companies, and individual clients.

## Features
- Public pages: Home, How It Works, Equipment Marketplace, Equipment Detail, Contact.
- User registration/login/logout with account type selection.
- Account-type dashboard redirection after login.
- Equipment categories and listings with pricing and location.
- Booking requests with status workflow and date validation.
- Django admin support for key models.
- Seed command for sample categories and equipment.
- Basic test coverage for core models and redirects.

## Tech Stack
- Python
- Django
- SQLite (local development)
- Django Templates
- HTML + CSS (no React)

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```
5. Seed sample data:
   ```bash
   python manage.py seed_data
   ```
6. Start development server:
   ```bash
   python manage.py runserver
   ```

## Core Data Models
- `User` (custom auth model with account types)
- `EquipmentCategory`
- `Equipment`
- `BookingRequest`

## Notes
- Equipment Owner dashboard shows owned equipment and incoming booking requests.
- Contractor dashboard shows available equipment and submitted requests.
- Uploaded photos are stored in `media/equipment_photos/`.


## Local verification commands
Run these commands from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py test
python manage.py runserver
```
