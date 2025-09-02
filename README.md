# Multi-Tenant E-commerce Platform

A robust, production-ready multi-tenant e-commerce platform built with Django and Django REST Framework. This platform supports multiple stores (tenants) on a single deployment, with isolated users, products, orders, and marketplace logic per tenant. It features JWT authentication, Paymob payment integration, and a modular, scalable architecture.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Core Apps](#core-apps)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Multi-Tenancy](#multi-tenancy)
- [Paymob Integration](#paymob-integration)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- **Multi-tenancy**: Each tenant (store) has isolated data and custom domain support.
- **Custom User Model**: Users are linked to tenants and support multiple roles (customer, seller, admin).
- **Marketplace Logic**: Buyers and sellers, product listings, orders, carts, and reviews.
- **Order Management**: Cart, checkout, address, and order tracking per tenant.
- **JWT Authentication**: Secure API access with Djoser and SimpleJWT.
- **REST API**: Built with Django REST Framework for easy integration.
- **Paymob Payment Integration**: Webhook support for payment status updates.
- **Celery Support**: For background tasks (e.g., order processing, notifications).

---

## Project Structure
```
├── apps/
│   ├── accounts/      # User management and authentication
│   ├── marketplace/   # Buyer/seller profiles, marketplace logic
│   ├── orders/        # Orders, carts, addresses
│   ├── products/      # Products, collections, reviews
│   └── tenancy/       # Tenant model, middleware
├── project/
│   ├── settings/      # Django settings (base, dev, prod)
│   ├── urls.py        # Root URL configuration
│   ├── celery.py      # Celery configuration
│   └── ...
├── .env               # Environment variables
├── manage.py          # Django management script
```

---

## Core Apps

### `tenancy`
- Manages tenants (stores), each with a unique domain and isolated data.
- `Tenant` model, `TenantMiddleware` for request routing.

### `accounts`
- Custom `User` model (extends `AbstractUser`), linked to a tenant.
- User roles: customer, seller, admin.
- JWT authentication (SimpleJWT), Djoser for user management.

### `marketplace`
- Buyer and seller profiles (linked to users and tenants).
- Seller ratings, payout info, loyalty points for buyers.

### `products`
- Product catalog, collections, product images, reviews.
- Products linked to sellers and tenants.

### `orders`
- Order placement and tracking, order items, carts, addresses.
- Payment status, Paymob integration fields.

---

## Installation & Setup

### Docker Setup

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   This will start the following services:
   - **web** (Django app) on [http://localhost:9000](http://localhost:9000)
   - **db** (Postgres) on port 5432
   - **redis** on port 6379

2. **Environment Variables:**
   - Ensure you have a valid `.env` file in the project root (see [Environment Variables](#environment-variables)).

3. **Stopping the services:**
   ```bash
   docker-compose down
   ```

You can still use the manual setup steps below if you prefer not to use Docker.

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd e-commerce
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in values (see [Environment Variables](#environment-variables)).

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## Environment Variables

The project uses a `.env` file for sensitive settings. Example variables:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
PAYMOB_HMAC=your-paymob-hmac
```

---

## Usage
- Access the API at `http://localhost:9000/api/` (if using Docker) or `http://localhost:8000/api/` (if running locally)
- Use the Django admin at `http://localhost:9000/admin/` (Docker) or `http://localhost:8000/admin/` (local)
- Register/login users via the API (Djoser endpoints)
- Each request is routed to the correct tenant via `TenantMiddleware` (based on domain or header)

---

## API Documentation
- Full API endpoint documentation is available in [API_DOCUMENTATION.txt](./API_DOCUMENTATION.txt).
- Main API root: `/api/`
- Authentication endpoints: `/auth/` (Djoser JWT)
- Example endpoints:
  - `/api/accounts/users/` — List users
  - `/api/tenants/` — Tenant management
  - `/api/products/` — Product catalog
  - `/api/orders/` — Orders and payments

See the documentation file for request/response details, permissions, and all available endpoints.

---

## Multi-Tenancy
- Each tenant is a store with its own users, products, and orders.
- `TenantMiddleware` ensures data isolation per request.
- Users are always linked to a tenant.

---

## Paymob Integration
- Webhook endpoint for Paymob payment notifications.
- Handles both GET and POST webhooks, with flexible field extraction and HMAC verification.
- See `orders/views.py` for Paymob webhook logic.

---

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

---

## License
MIT License

---

## Notes
- For production, set `DEBUG=False` and configure proper `ALLOWED_HOSTS`.
- For Celery, configure a broker (e.g., Redis) and run the worker with `celery -A project worker -l info`.
